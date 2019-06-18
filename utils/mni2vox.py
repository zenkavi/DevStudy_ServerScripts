#Translated from http://www.alivelearn.net/?p=1434

import numpy as np

def mni2vox(mni, T):
    mni = mni.extend([1])
    coordinate = np.round(np.matmul(mni,np.transpose(np.linalg.inv(T)))[:-1])
    return coordinate
