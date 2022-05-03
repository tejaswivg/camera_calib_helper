"""Script to visualize wand calibration data."""
import json
import re
import matplotlib.pyplot as plt

def get_cam(cam):
    pattern = re.compile(cam+" to .*")
    return [i for i in calib_data['pairwise transforms'] if pattern.match(i)]
    

calib_data = json.load(open('calibration_data.json', 'r'))
# TODO invert cam10 to cam16 translations
cams_to_invert = ["cam"+str(i) for i in range(10, 17)]

for i in cams_to_invert:
    relative_to_cam = get_cam(i)
    # TODO negate x,y,z translations
    print(i)
    print(relative_to_cam)

# TODO get translations quadrant-wise (cam1, cam4 , cam8, cam12)
# quadrant1, quadrant2, quadran3, quadrant4 = [re.compile("cam1 to.*"), re.compi

relative_to_cam1 = get_cam("cam1")
rt = [calib_data["pairwise transforms"][i] for i in relative_to_cam1]
translations = [i['relative tVec'] for i in rt]
fig = plt.figure()
ax = plt.axes(projection='3d')
x = [i[0] for i in translations]
y = [i[1] for i in translations]
z = [i[2] for i in translations]
for i in range(len(x)):
    ax.scatter(x[i], y[i], z[i], color = 'b')
    ax.text(x[i], y[i], z[i], relative_to_cam1[i], size=10, zorder=1, color='k')
# ax.scatter3D(x, y, z)
fig.show()
input()
