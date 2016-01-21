### ndio membrane segmentation imports
import ndio
print "ndio version: %s" % (ndio.version)

import ndio.remote.OCP as OCP
oo = OCP()

import ndio.remote.OCPMeta as NDLIMS
nn = NDLIMS()
###

### Watershed segmentation imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.morphology import closing
from skimage.morphology import binary_dilation
from skimage.morphology import binary_erosion
from skimage.filters.rank import threshold
from skimage.exposure import rescale_intensity
###

print "Done importing packages"

#########
# ndio demo for membrane segmentation
#########
'''
# Gather membrane data from OCP server

tokens = oo.get_public_tokens()
print len(tokens)

image_token = 'kasthuri11cc'
annotation_token = 'cv_kasthuri11_membrane_2014'

channel_ROI = nn.get_metadata('cv_kasthuri11_membrane_2014')['channels']

membrane_group_ROI = channel_ROI['image']['rois']['ac4']

membrane_query = {
    'token': 'cv_kasthuri11_membrane_2014',
    'channel': 'image',
    'x_start': membrane_group_ROI['x'][0],
    'x_stop': membrane_group_ROI['x'][1],
    'y_start': membrane_group_ROI['y'][0],
    'y_stop': membrane_group_ROI['y'][1],
    'z_start': membrane_group_ROI['z'][0],
    'z_stop': membrane_group_ROI['z'][1],
    'resolution': membrane_group_ROI['resolution'],
    }

print "Getting images"
membrane_images = oo.get_cutout(**membrane_query)
'''

# Gather images from nXp_data.npy file
print "Getting images"
membrane_images = np.load('nXp_data.npy')

# Assigning one image from array to variable pre_image
pre_image = membrane_images[0]

########
# Binary closing on image
########
print "Running closing"

close_image = closing(pre_image, selem=np.ones((4,4)))

print "Running threshold"
binary_img = threshold(close_image, selem=np.ones((200,200)))
print close_image[0]

image = binary_img
foreground = 1 - image

# image = foreground

########
# Watershed segmentation
########
print "Running watershed"

# Now we want to separate the two objects in image
# Generate the markers as local maxima of the distance to the background
distance = ndi.distance_transform_edt(foreground) # parameter: sampling=[100,100])
print distance[0]
distance_float = rescale_intensity(distance, in_range='image', out_range='float')
print (distance_float)
markers = threshold(distance_float, selem=np.ones((10,10)))
labels =  watershed(distance, markers, mask=foreground)
#labels =  watershed(distance, markers, mask=image)

fig, axes = plt.subplots(ncols=3, figsize=(10, 10), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax0, ax1, ax2 = axes

ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('Overlapping objects')
ax1.imshow(distance, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('Distances')
ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('Separated objects')

for ax in axes:
    ax.axis('off')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=0.9, bottom=0, left=0,
                    right=1)

plt.show()
