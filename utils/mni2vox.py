import numpy as np

def mni2vox(mni, T):
    mni.extend([1])
    T = np.transpose(np.linalg.inv(T))
    vox = np.round(np.matmul(mni,T)[:-1])
    vox = [int(x) for x in vox]
    vox = tuple(vox)
    return vox
#Translated from http://www.alivelearn.net/?p=1434
