import pickle
import numpy as np
import os
import sys
import argparse

files = ['voc_ds.pkl', 'lfw_ds.pkl', 'indoorCVPR_09_ds.pkl']

parser = argparse.ArgumentParser(description='check Original dataset and annotation into pickle')
parser.add_argument('--ds_file', '-d', type=str, default='voc_ds.pkl')
args = parser.parse_args()


def readpkl(f):
    if os.path.exists(f):
        with open(f,'rb') as fo:
            print("reading:%s"%f)
            image=pickle.load(fo)
        return image
    else:
        return None

def new_area(num, nptype, shapes):
    if len(shapes) == 2:
        image = np.zeros(
                num * np.prod(shapes[1:]),
                dtype=nptype
            ).reshape(
                -1,shapes[1]
            )
    elif len(shapes) == 4:
        image = np.zeros(
                num * np.prod(shapes[1:]),
                dtype=nptype
            ).reshape(
                -1,shapes[1],shapes[2],shapes[3]
            )
    return image

# PASS:1
print('\n# PASS:1')
image_posiN=0
image_negaN=0
image_ambiN=0
for f in files:
    image = readpkl(f)
    if image is None:
        print('Warning: %s not found, skip.'%f)
        continue
    else:
        print('->analizing %s.'%f)
        for k in image.keys():
            if str(k) == 'image_posi':
                image_posiN+=len(image[k])
            elif str(k) == 'image_nega':
                image_negaN+=len(image[k])
            elif k == 'image_ambi':
                image_ambiN+=len(image[k])
            elif k == 'truth_posi':
                truth_posi_shape=image[k].shape
print('posiN/negaN/ambiN = %d/%d/%d'%(image_posiN,image_negaN,image_ambiN))

print('\n# SETUP TOTAL AREA')
image_posi = new_area(image_posiN, np.uint8, image['image_posi'].shape)
print 'image_posi.shape',image_posi.shape

image_nega = new_area(image_negaN, np.uint8, image['image_nega'].shape)
print 'image_nega.shape',image_nega.shape

image_ambi = new_area(image_ambiN, np.uint8, image['image_ambi'].shape)
print 'image_ambi.shape',image_ambi.shape

truth_posi = new_area(image_posiN, np.int32, truth_posi_shape)
print 'truth_posi.shape',truth_posi.shape

truth_nega = new_area(image_negaN, np.int32, truth_posi_shape)
print 'truth_nega.shape',truth_nega.shape

truth_ambi = new_area(image_ambiN, np.int32, truth_posi_shape)
print 'truth_ambi.shape',truth_ambi.shape

print('\n# PASS:2')
image_posiN=0
image_negaN=0
image_ambiN=0
truth_posiN=0
truth_negaN=0
truth_ambiN=0
for f in files:
    image = readpkl(f)
    if image is None:
        print('Warning: %s not found, skip.'%f)
        continue
    else:
        print('->stacking %s.'%f)
        for k in image.keys():
            if str(k) == 'image_posi':
                num=len(image[k])
                image_posi[image_posiN:image_posiN+num]=image[k].copy()
                image_posiN+=num
            elif str(k) == 'image_nega':
                num=len(image[k])
                image_nega[image_negaN:image_negaN+num]=image[k].copy()
                image_negaN+=num
            elif k == 'image_ambi':
                num=len(image[k])
                image_ambi[image_ambiN:image_ambiN+num]=image[k].copy()
                image_ambiN+=num
            elif k == 'truth_posi':
                num=len(image[k])
                truth_posi[truth_posiN:truth_posiN+num]=image[k].copy()
                truth_posiN+=num
            elif k == 'truth_nega':
                num=len(image[k])
                truth_nega[truth_negaN:truth_negaN+num]=image[k].copy()
                truth_negaN+=num
            elif k == 'truth_ambi':
                num=len(image[k])
                truth_ambi[truth_ambiN:truth_ambiN+num]=image[k].copy()
                truth_ambiN+=num

print('image posiN/negaN/ambiN = %d/%d/%d'%(image_posiN,image_negaN,image_ambiN))
print('truth posiN/negaN/ambiN = %d/%d/%d'%(truth_posiN,truth_negaN,truth_ambiN))

print('\n# STATISTICS NEGA/POSI TRUTH BY 1.0/0.0')
truth_posi_zeros = len(truth_posi[truth_posi==0.])
truth_nega_zeros = len(truth_nega[truth_nega==0.])
truth_ambi_zeros = len(truth_ambi[truth_ambi==0.])
truth_posi_nonzs = np.count_nonzero(truth_posi)
truth_nega_nonzs = np.count_nonzero(truth_nega)
truth_ambi_nonzs = np.count_nonzero(truth_ambi)
print('truth posi 1.0/0.0=%8d/%8d'%(truth_posi_nonzs,truth_posi_zeros))
print('truth nega 1.0/0.0=%8d/%8d'%(truth_nega_nonzs,truth_nega_zeros))
print('truth ambi 1.0/0.0=%8d/%8d'%(truth_ambi_nonzs,truth_ambi_zeros))

using_posi = image_posiN
using_nega = int(truth_posi_nonzs / truth_posi.shape[1] - truth_posi_zeros / truth_posi.shape[1])
print('Usable leaning images is using_posi/using_nega = %d/%d'%(using_posi,using_nega))

using_posi_test = int(using_posi/10)
using_nega_test = int(using_nega/10)
using_posi_train= using_posi - using_posi_test
using_nega_train= using_nega - using_nega_test
print('Separate for train posi/nega = %d/%d'%(using_posi_train,using_nega_train))
print('Separate for test  posi/nega = %d/%d'%(using_posi_test ,using_nega_test))
using_trainN = using_posi_train + using_nega_train
using_testN  = using_posi_test  + using_nega_test
print('\n# Finally images train/test = %d/%d'%(using_trainN,using_testN))

# *[12]_train are np.slice type
# To copy into train_image and train_truth
# size of image posi and truth posi is same, 
#--------------------------------- train image
# image posi [ p1_train p2_test ]
#              |
# train image[ x1_posi  x2_nega ]
#                      /
# image nega [ n1_train n2_test ]
#--------------------------------- train truth
# truth posi [ p1_train p2_test ]
#              |
# train truth[ x1_posi  x2_nega ]
#                      /
# truth nega [ n1_train n2_test ]
#---------------------------------

# To copy into test_image and test_truth
#--------------------------------- test image
# image posi [ p1_train p2_test ]
#                      /
# test  image[  X1_posi X2_nega ]
#                       |
# image nega [ n1_train n2_test ]
#--------------------------------- test truth
# truth posi [ p1_train p2_test ]
#                      /
# test  truth[  X1_posi X2_nega ]
#                       |
# truth nega [ n1_train n2_test ]
#---------------------------------

#
p1_train = np.s_[                0 : using_posi_train ]
p2_test  = np.s_[ using_posi_train : using_posi_train + using_posi_test ]
n1_train = np.s_[                0 : using_nega_train ]
n2_test  = np.s_[ using_nega_train : using_nega_train + using_nega_test ]
#
x1_posi  = np.s_[                0 : using_posi_train ]
x2_nega  = np.s_[ using_posi_train : using_posi_train + using_nega_train]
#
X1_posi  = np.s_[                0 : using_posi_test ]
X2_nega  = np.s_[ using_posi_test  : using_posi_test  + using_nega_test]

print('\n# RECONSTRUCTURE PROCESS BY BELOW SLICE..')
print 'p1_train:' ,p1_train
print 'p2_test :' ,p2_test
print 'n1_train:' ,n1_train
print 'n2_test :' ,n2_test
print 'x1_posi :' ,x1_posi
print 'x2_nega :' ,x2_nega
print 'X1_posi :' ,X1_posi
print 'X2_nega :' ,X2_nega

train_nonz = np.count_nonzero(truth_posi[p1_train])
train_zero = np.prod(truth_nega[n1_train].shape) + np.prod(truth_posi[p1_train].shape) - train_nonz
train_diff = int((train_nonz - train_zero)/truth_nega.shape[1])
print('train nonz/zero(trimNegaImages)=%d/%d/%d'%(train_nonz,train_zero,train_diff))

test_nonz = np.count_nonzero(truth_posi[p2_test])
test_zero = np.prod(truth_nega[n2_test].shape)
test_diff = int((test_nonz - test_zero)/truth_nega.shape[1])
print('test  nonz/zero(trimNegaImages)=%d/%d/%d'%(test_nonz,test_zero,test_diff))

# total areas
train_image = new_area(using_trainN, np.uint8, image_posi.shape)
train_truth = new_area(using_trainN, np.int32, truth_posi.shape)
test_image  = new_area(using_testN , np.uint8, image_posi.shape)
test_truth  = new_area(using_testN , np.int32, truth_posi.shape)

# Coping
train_image[x1_posi] = image_posi[p1_train]
train_image[x2_nega] = image_nega[n1_train]
train_truth[x1_posi] = truth_posi[p1_train]
train_truth[x2_nega] = truth_nega[n1_train]

test_image[X1_posi]  = image_posi[p2_test]
test_image[X2_nega]  = image_nega[n2_test]
test_truth[X1_posi]  = truth_posi[p2_test]
test_truth[X2_nega]  = truth_nega[n2_test]

print 'train_image.shape :', train_image.shape
print 'train_truth.shape :', train_truth.shape
print 'test_image.shape  :', test_image.shape
print 'test_truth.shape  :', test_truth.shape
train_nonz = np.count_nonzero(train_truth)
train_alls = np.prod(train_truth.shape)
nonz_ratio = float(train_nonz)/float(train_alls)
print('train data nonzero/all ratio = %d/%d = %5.2f'%(train_nonz, train_alls, 100.*nonz_ratio))
test_nonz = np.count_nonzero(test_truth)
test_alls = np.prod(test_truth.shape)
nonz_ratio = float(test_nonz)/float(test_alls)
print('test  data nonzero/all ratio = %d/%d = %5.2f'%(test_nonz, test_alls, 100.*nonz_ratio))

print('\n# SAVING')
with open('image.pkl','wb') as f:
    print('  %s'%'image.pkl')
    image_all = {
        'train': train_image,
        'test':  test_image
        }
    pickle.dump(image_all,f)

with open('label.pkl','wb') as f:
    print('  %s'%'label.pkl')
    truth_all = {
        'train': train_truth,
        'test':  test_truth
        }
    pickle.dump(truth_all,f)

sys.exit(1)