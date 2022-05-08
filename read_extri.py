import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

import sys 
sys.path.append('D:\\code\\EasyMocap\\easymocap\\mytools\\')

import camera_utils as cu

if __name__ == "__main__":
    cams = cu.read_camera('intri.yml', 'extri.yml')
    cams.pop('basenames')
    for i in cams.keys():
        try:
            print('current camera' + str(i))
            translation = cams[i]['T'].flatten()
            rotation = cams[i]['R']
            position = np.matrix(rotation, dtype = np.float32)  * np.matrix(translation, dtype = np.float32).T
            position = position.flat
            print(str(position[0])+','+ str(position[1])+',' + str(position[2]))
            ax.scatter(position[0], position[1], position[2])
            ax.text(position[0],position[1],position[2] , i)
        except ValueError:
            print(position)
        except BaseException as err:
            print(err)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
#import pickle
#pickle.dump(fig, open('cams_plot.fig.pickle', 'wb')) # This is for Python 3 - py2 may need `file` instead of `open`
