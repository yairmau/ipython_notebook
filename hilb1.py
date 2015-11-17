import numpy as np

def rot(alpha):
    return np.array([[np.cos(alpha),-np.sin(alpha)],
                     [np.sin(alpha), np.cos(alpha)]])

alpha = np.pi/2.0
r = np.round(rot(alpha),1)
print r

v = np.array([1,0])
print np.dot(-r,v)