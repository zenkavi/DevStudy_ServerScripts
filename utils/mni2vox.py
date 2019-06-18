#Translated from http://www.alivelearn.net/?p=1434

import numpy as np

def mni2vox(mni, T):
    mni.extend([1])
    print(mni)
    print(T)
    T = np.transpose(np.linalg.inv(T))
    print(T)
    #coordinate = np.round(np.matmul(mni,T)[:-1])
    #return coordinate
