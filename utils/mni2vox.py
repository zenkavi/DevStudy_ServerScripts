#Translated from http://www.alivelearn.net/?p=1434

import numpy as np

def mni2vox(mni, T):
    mni.extend([1])
    T = np.transpose(np.linalg.inv(T))
    coordinate = np.round(np.matmul(mni,T)[:-1])
    return coordinate
