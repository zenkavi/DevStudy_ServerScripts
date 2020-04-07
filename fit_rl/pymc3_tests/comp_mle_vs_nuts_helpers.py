import numpy as np
import pandas as pd
import scipy
import pymc3 as pm
import theano
import theano.tensor as tt

def generate_data(alpha, beta, n=100,
                  p_r={'high_var': [.95, .05], 'low_var': [.5,.5]},
                  rs = np.array(([5.0, -495.0],[-5.0, 495.0],[10.0, -100.0],[-10.0, 100.0])),
                  sQ = np.zeros((4, 2))
                 ):

    # Need to denote both machine type and action

    # Pre-specify machines for each trial in a randomly balanced manner
    if n%4 != 0:
        print("Number of trials is not divisable by 4.\nCreating trials for %s trials."%(str(n-(n%4))))
        n = n-(n%4)

    machs = np.array([0,1,2,3])
    machs = np.tile(machs, int(n/4))
    np.random.shuffle(machs)

    # Initialize empty array that will be populated in the loop based on Q values
    acts = np.zeros(n, dtype=np.int)

    # Generate by coin flip for machine with differing probabilities and outcomes
    rews = np.zeros(n, dtype=np.int)

    # Stores the expected value for each of 4 machines in each trial for each action
    Qs = np.zeros((n, 4, 2))

    # Initialize Q table
    # Denotes expected value of each action
    # Should look like [0, 0] for each machine
    # *** The expected value of not playing should not change from 0! ***
    # Could these initial expected values/beliefs also be estimated from data?
    # E.g. what if kids have more optimistic priors about each machine though they learn at the same rate
    Q = sQ.copy()

    for i in range(n):

        cur_machine = machs[i]

        # Apply the Softmax transformation
        exp_Q = np.exp(beta*Q[cur_machine])
        prob_a = exp_Q / np.sum(exp_Q)

        # Simulate choice
        a = np.random.choice([0, 1], p=prob_a)

        # Simulate reward if machine is played
        if a == 1:

            # Before sampling reward determine which variance condition machine is in
            if cur_machine>1:
                cur_p = 'low_var'
            else:
                cur_p = 'high_var'

            # Sample reward for current machine given its reward probs and outcome options
            r = np.random.choice(rs[cur_machine], p = p_r[cur_p])

            # Update Q table only if the machine is played
            # And only the value of playing NOT of not playing
            Q[cur_machine][a] = Q[cur_machine][a] + alpha * (r - Q[cur_machine][a])

        # If the machine is not played then Q remains unchanged and no reward is received
        else:
            r = 0.0

        # Store values
        acts[i] = a
        rews[i] = r
        #Qs[i] = Q.copy()
        Qs[i] = Q

    return machs, acts, rews, Qs

def llik_td_vectorized(x, *args):
    # Extract the arguments as they are passed by scipy.optimize.minimize
    alpha, beta = x
    machines, actions, rewards = args
    n = len(actions)

    # Create a list with the Q values of each trial
    Qs = np.zeros((n, 4, 2), dtype=np.float)

    # The last Q values were never used, so there is no need to compute them
    for t, (m, a, r) in enumerate(zip(machines[:-1], actions[:-1], rewards[:-1])):
        Qs[t+1] = Qs[t]
        Qs[t+1, m, a] = Qs[t, m, a] + alpha * (r - Qs[t, m, a])
        Qs[t+1, m, 1-a] = Qs[t, m, 1-a]
        #print('t: %s, m: %s, a: %s, r: %s, Q:[%s, %s]'%(str(t), str(m), str(a), str(r), str(Qs[t,m,0]), str(Qs[t,m, 1])))

    # Apply the softmax transformation in a vectorized way
    idx = list(zip(range(n),machines))
    obs_Qs = [Qs[i] for i in idx]
    Qs_ = np.array(obs_Qs) * beta
    log_prob_actions = Qs_ - scipy.special.logsumexp(Qs_, axis=1)[:, None]

    # Return the log_prob_actions for the observed actions
    log_prob_obs_actions = log_prob_actions[np.arange(n), actions]
    return -np.sum(log_prob_obs_actions[1:])

def update_Q(machine, action, reward,
             Q,
             alpha):
    Q = tt.set_subtensor(Q[machine, action], Q[machine, action] + alpha * (reward - Q[machine, action]))
    return Q

def theano_llik_td(alpha, beta, machines, actions, rewards, n=120):
    # Transform the variables into appropriate Theano objects
    machines_ = theano.shared(np.asarray(machines, dtype='int16'))
    actions_ = theano.shared(np.asarray(actions, dtype='int16'))
    rewards_ = theano.shared(np.asarray(rewards, dtype='int16'))

    # Initialize the Q table
    Qs = tt.zeros((4,2), dtype='float64')

    # Compute the Q values for each trial
    Qs, updates = theano.scan(
        fn=update_Q,
        sequences=[machines_, actions_, rewards_],
        outputs_info=[Qs],
        non_sequences=[alpha])

    int_Qs = tt.zeros((1, 4,2), dtype='float64')

    Qs = tt.concatenate((int_Qs, Qs), axis=0)

    # Apply the softmax transformation
    idx = list(zip(range(n),machines)) #list of tuples
    obs_Qs = [Qs[i] for i in idx]
    Qs_ = obs_Qs * beta
    log_prob_actions = Qs_ - pm.math.logsumexp(Qs_, axis=1)

    # Calculate the negative log likelihod of the observed actions
    log_prob_actions = log_prob_actions[tt.arange(actions_.shape[0]), actions_]
    return tt.sum(log_prob_actions[1:])

# Wrap all the steps pre output into a function
def get_mle_nuts_est(true_alpha, true_beta, n=120, mle_niters = 50):

    # Generate data
    machines, actions, rewards, all_Qs = generate_data(true_alpha, true_beta, n)
    true_llik = llik_td_vectorized([true_alpha, true_beta], *(machines, actions, rewards))

    # MLE estimate starting from true value
    x0 = [true_alpha, true_beta]
    result = scipy.optimize.minimize(llik_td_vectorized, x0, args=(machines, actions, rewards), method='BFGS')
    mle_alpha_ts = result.x[0]
    mle_beta_ts = result.x[1]
    mle_llik_ts = result.fun

    # MLE estimate starting from value sampled from prior
    print("Starting MLE iterations with random starts...")

    mle_iters = pd.DataFrame([])
    for i in range(mle_niters):
        random_alpha_start = np.random.beta(1,1)
        random_beta_start = scipy.stats.halfnorm(scale=10).rvs()
        x0 = [random_alpha_start, random_beta_start]
        result = scipy.optimize.minimize(llik_td_vectorized, x0, args=(machines, actions, rewards), method='BFGS')
        cur_alpha_est = result.x[0]
        cur_beta_est = result.x[1]
        cur_llik = result.fun
        mle_iters = mle_iters.append({"true_alpha": true_alpha,
                                      "true_beta": true_beta,
                                      'random_alpha_start':random_alpha_start,
                                      'random_beta_starts': random_beta_start,
                                      'cur_alpha_est': cur_alpha_est,
                                      'cur_beta_est': cur_beta_est,
                                      'cur_llik': cur_llik}, ignore_index=True)

    print("Done with MLE iterations with random starts.")

    mle_alpha_ave = np.mean(mle_iters.cur_alpha_est)
    mle_alpha_std = np.std(mle_iters.cur_alpha_est)
    mle_beta_ave = np.mean(mle_iters.cur_beta_est)
    mle_beta_std = np.std(mle_iters.cur_beta_est)
    mle_llik_ave = np.mean(mle_iters.cur_llik)
    mle_llik_std = np.std(mle_iters.cur_llik)

    # NUTS estimate
    actions_ = theano.shared(np.asarray(actions, dtype='int16'))
    with pm.Model() as m:
        alpha = pm.Beta('alpha', 1, 1)
        beta = pm.HalfNormal('beta', 10)
        like = pm.Potential('like', theano_llik_td(alpha, beta, machines, actions, rewards, n))
        tr = pm.sample()

    nuts_alpha_ave = np.mean(tr.alpha)
    nuts_beta_ave = np.mean(tr.beta)
    nuts_alpha_std = np.std(tr.alpha)
    nuts_beta_std = np.std(tr.beta)
    nuts_llik = llik_td_vectorized([nuts_alpha_ave, nuts_beta_ave], *(machines, actions, rewards))

    # Output:
    est_df = pd.DataFrame(data={"true_alpha": true_alpha,
                                "true_beta": true_beta,
                                "true_llik": true_llik,
                                "mle_alpha_ts": mle_alpha_ts,
                                "mle_beta_ts": mle_beta_ts,
                                "mle_llik_ts": mle_llik_ts,
                                "mle_alpha_ave":mle_alpha_ave,
                                "mle_beta_ave": mle_beta_ave,
                                "mle_alpha_std":mle_alpha_std,
                                "mle_beta_std": mle_beta_std,
                                "mle_llik_ave": mle_llik_ave,
                                "mle_llik_std":mle_llik_std,
                                "nuts_alpha_ave": nuts_alpha_ave,
                                "nuts_beta_ave": nuts_beta_ave,
                                "nuts_alpha_std": nuts_alpha_std,
                                "nuts_beta_std": nuts_beta_std,
                                "nuts_llik": nuts_llik}, index=[0])

    nuts_posteriors = pd.DataFrame(data={"true_alpha": true_alpha,
                                         "true_beta": true_beta,
                                         "alpha": pd.Series(tr.get_values('alpha')),
                                        "beta": pd.Series(tr.get_values('beta'))})

    #return {"est_df": est_df, "mle_iters": mle_iters, "nuts_posteriors": nuts_posteriors}
    return (est_df,  mle_iters, nuts_posteriors)
