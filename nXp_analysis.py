### ndio membrane segmentation imports
import ndio
print "ndio version: %s" % (ndio.version)

import ndio.remote.OCP as OCP
oo = OCP()

import ndio.remote.OCPMeta as NDLIMS
nn = NDLIMS()
###

### Python image processing imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
###

### Watershed segmentation imports
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.morphology import closing
from skimage.morphology import binary_dilation
from skimage.morphology import binary_erosion
from skimage.filters.rank import threshold
from skimage.exposure import rescale_intensity
from skimage.filters import threshold_otsu
###

### Gala imports
import gala.evaluate as ev
###

# Finished importing
print "Done importing packages"

# Sets up results.txt file to store output data from evaluation
outFile = open('results.txt', 'w')

#########
# ndio to attain membrane segmentation data
#########

############### sparse arrays for sweeping parameters
### parameters change by selected step for given range
footArr = [24, 20, 21]
filtArr = [5, 6, 7, 8]
peakArr = [1, 2, 5, 11]


# Gather images from nXp_data.npy file
print "Getting images"
membrane_images = np.load('nXp_data.npy')
membrane_ground = np.load('nXp_ground.npy')

# Assigning one image from array to variable pre_image for first 50 images
for index in range(0, 50):

	pre_image = membrane_images[index]

# Closing footprin parameter.
	for foot in footArr:
		########
		# Binary closing on image
		########
		# print "Running closing"
		close_image = closing(pre_image, selem=np.ones((foot,foot)))

		for filt in filtArr:

			# print "Running median filter"
			# Remove of white speckles of noise
			img_med = ndi.median_filter(close_image, size=filt)

			# print "Running threshold"
			threshold = threshold_otsu(img_med)
			binary_img = img_med > threshold

			# make image into binary_img and invert it
			image = binary_img
			foreground = 1 - image

			########
			# Watershed segmentation
			########
			# print "Running watershed"

			# Now we want to separate the two objects in image
			# Generate the markers as local maxima of the distance to the background
			distance = ndi.distance_transform_edt(foreground)
			distance_float = rescale_intensity(distance, in_range='image', out_range='float')

			# Changes local mas peak paramater
			for peakPrint in peakArr:

				local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((peakPrint, peakPrint)), labels=foreground)
				markers = ndi.label(local_maxi)[0] #[0]

				labels =  watershed(foreground, markers, mask=foreground)

				######## Get the watershed evaluation
				split_eval = ev.split_vi(labels, membrane_ground[index])
				adjusted_rand = ev.adj_rand_index(labels, membrane_ground[index])
				fm = ev.fm_index(labels, membrane_ground[index])
				outFile.write(str(index) + "_" + str(foot) + "_" + str(filt) + "_" + str(peakPrint) + " " + str(split_eval) + " " + str(adjusted_rand) + " " + str(fm) + "\n")
