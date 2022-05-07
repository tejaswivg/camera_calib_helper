"""Script to visualize wand calibration data."""
import json
import re
import matplotlib.pyplot as plt


#def get_cam(cam):
#    """Get transforms relative to camera 'cam'."""
#    pattern = re.compile("("+cam+") to (cam.*)")
#    relative_transforms = []
#    for i in calib_data['pairwise transforms']:
#        matches = pattern.match(i)
#        if(matches is not None):
#            print('src' + matches[1])
#            print('dest' + matches[2])
#            relative_transforms.append(i)
#    return relative_transforms


updated_transforms = dict()

def get_cam(cam_src, cam_dest):
    """Should return translation for given src, dest pair. 
    search in both the json and the inverted transforms"""
    pattern_string = f'cam{cam_src} to cam{cam_dest}'
    translation = None
    try:
        translation = updated_transforms[pattern_string]["relative tVec"]
    except TypeError:
        # ugly hack
        translation = updated_transforms[pattern_string]
    return translation


def parse_cam_names(camAtoB):
    pattern = re.compile("cam([0-9]+) to cam([0-9]+)")
    matched = pattern.match(camAtoB)
    return matched.group(1), matched.group(2)

f = open('calibration_data.json', 'r')
calib_data = json.load(f)

# TODO invert cam10 to cam16 translations
# camX to camY invert where Y< X
cams_to_invert = ["cam"+str(i) for i in range(10, 17)]

inverted_transforms = dict()
for i in cams_to_invert:
    for x, y in calib_data["pairwise transforms"].items():
        cam_src, cam_dest = parse_cam_names(x)
        if(x.startswith(i) and (int(cam_src) > int(cam_dest))):
            # invert translation and set
            new_key = "cam"+cam_dest+" to "+"cam"+cam_src
            inverted_transforms[new_key] = [-i for i in y["relative tVec"]]
    # print(relative_to_cam)

updated_transforms = {**calib_data["pairwise transforms"], **inverted_transforms}


def inclusive_range(start, end):
    return range(start, end+1)

abs_cam_positions = list()
# TODO get translations quadrant-wise (cam1, cam4 , cam8, cam12)
# and 'adjust' them i.e. make them relative to the first cam of the quadrant
quadrants = [(1, 4), (5, 8), (9, 12), (13, 16)]
[abs_cam_positions.append(i) for i in [[0.0, 0.0, 0.0], get_cam(1,5), get_cam(1,9), get_cam(1,13)]]
for i in quadrants:
    print("current quadrant " + str(i[0]))
    cam_src = i[0]
    cam_dest = [cam_idx for cam_idx in inclusive_range(*i)]
    # TODO: there might be a bug here
    if(cam_src == 1):
        pos_src = [0.0, 0.0, 0.0]
        #abs_cam_positions.append(pos_src)
    else:
        pos_src = get_cam(1, i[0])
        #abs_cam_positions.append(pos_src)

    # convert to absolute translations 
    for cam_idx in cam_dest:
        if cam_src == cam_idx:
            continue
        print(f'{cam_src} : {cam_idx}')
        pos = get_cam(cam_src, cam_idx)
        abs_cam_positions.append([ i  for i,j in zip(pos,pos_src)])

    #relative_to_cam_i = get_cam("cam"+str(i))
    #print(relative_to_cam_i)

#relative_to_cam1 = get_cam("cam1")
#rt = [calib_data["pairwise transforms"][i] for i in relative_to_cam1]
#translations = [i['relative tVec'] for i in rt]
translations = abs_cam_positions
fig = plt.figure()
ax = plt.axes(projection='3d')
x = [i[0] for i in translations]
y = [i[1] for i in translations]
z = [i[2] for i in translations]
#for i in range(len(x)):
#    ax.scatter(x[i], y[i], z[i], color = 'b')
#    ax.text(x[i], y[i], z[i], i, size=10, zorder=1, color='k')
ax.scatter3D(x, y, z)
fig.show()
