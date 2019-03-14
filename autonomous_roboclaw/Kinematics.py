# -*- coding: utf-8 -*-
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink, DHLink
#from Link_FIXED import DHLink
import numpy as np

# Define the head servos based on Denavit-Hartenberg values

# measured values, in units mm and rad TODO more exact
rad90 = np.pi / 2.0  # 90 degree in radians

# head in relation to body
a1 = 0.0
d1 = 0.0
alpha1 = 0.0

# face in relation to head
a2 = 0.070
d2 = 0.020
alpha2 = rad90

# eye in relation to face
a3 = 0.030
d3 = 0.0  # variable == focal_lenght??
alpha3 = rad90
theta3 = 0.0

# TODO check ikpy does not support alpha/theta in DHLink??

# DH links semm not yet fully implemented in ikpy!!
dhlinks = [
    # OriginLink(), head is our origin at the moment!
    DHLink(
        name="head",
        d=d1,
        a=a1,
        #alpha=alpha1
        # theta variable
        # TODO bounds=(min,max)
    ),
    DHLink(
        name="face",
        d=d2,
        a=a2,
        #alpha=alpha2
        # theta variable
        # TODO bounds=(min,max)
    ),
    DHLink(
        name="eye",
        d=d3,
        a=a3,
        #alpha=alpha3,
        #theta=theta3
        # TODO bounds=(min,max)
    )
]

# TODO put our robo in URDF notation
ulinks = [
    OriginLink(),
    URDFLink(
      name="shoulder",
      translation_vector=[-10, 0, 5],
      orientation=[0, 1.57, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="elbow",
      translation_vector=[25, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="wrist",
      translation_vector=[22, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    )
    ]

robo_chain = Chain(name="robo_chain", links=ulinks)

robo_chain.forward_kinematics([0] * len(ulinks))

# test matrix, to check if defaults are as expected:
look_straight = [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]]

#robo__chain.inverse_kinematics(look_straight)

#import time
#time.sleep(1000)

if __name__ == '__main__':
    # show inverse kinematic
    import matplotlib.pyplot
    from mpl_toolkits.mplot3d import Axes3D
    ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
    robo_chain.plot(robo_chain.inverse_kinematics(look_straight), ax)
    matplotlib.pyplot.show()

