############################################################## 
# Licensed under the MIT License                             #
# Copyright (c) 2018 Stefan Hein Bengtson and Malte Pedersen #
# See the file LICENSE for more information                  #
##############################################################

import argparse
import os
import sys
from sklearn.externals import joblib

sys.path.append('../');
from source.Camera import Camera

# Description:
# Calibrates a camera using the images in the specified folder
# The parameters are saved in 'camera.pkl' in the same folder
#
# Example of usage:
# > $python calibrate_intrinsics.py -cs 9 6 -ss 0.935 -if ../data/checkerboard_images/ -it .jpg
#
#       -cs is the number of squares on the checkerboard. In the given example the checkerboard has 9x6 squares.
#       -ss is the size of the squares in centimeters
#       -if is the image-folder
#       -it is the image-type (.jpg, .png, etc.) 


# Terminal code running handling
ap = argparse.ArgumentParser();
ap.add_argument('-cs', '--checkerboardSize', nargs='+', type=int, help='number of squares on the checkerboard. E.g. [9 6] for a checkerboard that is 9 squares long and 6 squares wide.');
ap.add_argument('-ss', '--squareSize', help='size of the squares in centimeters');
ap.add_argument('-if', '--imageFolder', help='path to the folder containing the calibration images');
ap.add_argument('-it', '--imageType', help='type of image files. E.g. .png or .jpg');
ap.add_argument('-n_air', '--refractive_index_air', type=float, default=1.0, help='refractive index of air (default: 1.0)');
ap.add_argument('-n_acrylic', '--refractive_index_acrylic', type=float, default=1.49, help='refractive index of acrylic (default: 1.49)');
ap.add_argument('-n_water', '--refractive_index_water', type=float, default=1.33, help='refractive index of water (default: 1.33)');

args = vars(ap.parse_args());

if args.get('checkerboardSize', None) is None:
    print('Please specify checkerboard size');
    sys.exit();
else:
    checkerboardSize = tuple(args['checkerboardSize'])

if args.get('squareSize', None) is None:
    print('Please specify square size');
    sys.exit();
else:
    squareSize= float(args['squareSize'])

if args.get('imageFolder', None) is None:
    print('Please specify the path to the image folder');
    sys.exit();
else:
    imageFolder = args['imageFolder']

if args.get('imageType', None) is None:
    print('Please specify type of image (.jpg or .png)');
    sys.exit();
else:
    imageType = args['imageType']



# Refractive indices
n_air = args['refractive_index_air']
n_acrylic = args['refractive_index_acrylic']
n_water = args['refractive_index_water']

print('Calibrating camera using the following parameters:')
print(' - image folder: ' + imageFolder)
print(' - checkerboard size: ' + str(checkerboardSize))
print(' - square size: ' + str(squareSize))
print(' - refractive index of air: ' + str(n_air))
print(' - refractive index of acrylic: ' + str(n_acrylic))
print(' - refractive index of water: ' + str(n_water))
      
cam = Camera()
cam.set_refractive_indices(n_air, n_acrylic, n_water)
cam.calibrateFromFolder(imageFolder + '*' + imageType, checkerboardSize, squareSize, verbose=True)

print('Intrinsic: \n' + str(cam.K))
print('Distortion: \n' + str(cam.dist))

outputName = os.path.join(imageFolder, 'camera.pkl')
print('Saving camera to: ' + str(outputName))
joblib.dump(cam, outputName)
print('Done!')
