from gala import classify, morpho, features, agglo, evaluate as ev, optimized #imio
import numpy as np
from skimage.morphology import closing
from skimage.morphology import binary_dilation
from skimage.morphology import binary_erosion
from skimage.filters.rank import threshold
import matplotlib.pyplot as plt

# Gather images from nXp_data.npy file
print "Getting images"
membrane_images = np.load('nXp_data.npy')

pre_image = 255 * membrane_images[0]

min_seed_size = 5 #2
connectivity = 2
smooth_thresh = 0.02 #0.02

ws_train = morpho.watershed(pre_image,
connectivity=connectivity, smooth_thresh=smooth_thresh,
override_skimage=1,minimum_seed_size=min_seed_size) + 1
#ws_train = ws_train
fig, axes = plt.subplots(ncols=1, figsize=(8, 2.7), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax0 = axes

ax0.imshow(ws_train)#, cmap=plt.cm.spectral, interpolation='nearest')
ax0.set_title('Overlapping objects')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=0.9, bottom=0, left=0,
                    right=1)

plt.show()
