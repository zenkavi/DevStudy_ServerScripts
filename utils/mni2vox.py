import numpy as np
from copy import copy
def mni2vox(mni, T):
    mni_copy = copy(mni)
    mni_copy.extend([1])
    T = np.transpose(np.linalg.inv(T))
    vox = np.round(np.matmul(mni_copy,T)[:-1])
    vox = [int(x) for x in vox]
    vox = tuple(vox)
    return vox
#Translated from http://www.alivelearn.net/?p=1434
