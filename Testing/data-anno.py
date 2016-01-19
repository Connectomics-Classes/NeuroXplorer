### ndio membrane segmentation imports
import ndio
print ndio.version  # Prints version

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
###

#########
# ndio demo for membrane segmentation
#########
'''
If you're running your own OCP server locally for testing, you can specify a
different hostname (instead of http://openconnecto.me) like this:

oo = OCP('your_ip_or_hostname.com')
'''

'''
Now we're ready to download data. For this example, we'll download some data
and annotations from Kasthuri et al. Cell (2015). We can see a full list of
public data using ndio.remote.OCP.get_public_tokens(), but there are so many
that they'd fill the screen:
'''

tokens = oo.get_public_tokens()
print len(tokens)

image_token = 'kasthuri11cc'
annotation_token = 'kasthuri2015_ramon_v1'
segmentation_token = 'ac3ac4'

'''
Next we'll download a sample of data and ground-truth annotations from this
dataset. Some of you are researching membrane segmentation, and will want
to use this sample:
'''

channel_ROIs = nn.get_metadata(segmentation_token)['channels']

membrane_group_ROI = channel_ROIs['ac4_neuron_truth']['rois']['ac4']
membrane_query = {
    'token': 'ac3ac4',
    'channel': 'ac4_neuron_truth',
    'x_start': membrane_group_ROI['x'][0],
    'x_stop': membrane_group_ROI['x'][1],
    'y_start': membrane_group_ROI['y'][0],
    'y_stop': membrane_group_ROI['y'][1],
    'z_start': membrane_group_ROI['z'][0],
    'z_stop': membrane_group_ROI['z'][1],
    'resolution': membrane_group_ROI['resolution']
}

'''
Now you can retrieve your data by using your ROI bounds, and then requesting it
from OCP:
'''

membrane_anno = oo.get_cutout(**membrane_query)

membrane_query['token'] = 'kasthuri11cc'
membrane_query['channel'] = 'image'
membrane_query['resolution'] = 1

membrane_images = oo.get_cutout(**membrane_query)

########
# Watershed segmentation
########

image = membrane_images[0]

# Now we want to separate the two objects in image
# Generate the markers as local maxima of the distance to the background
distance = ndi.distance_transform_edt(image)
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((8, 8)),
                            labels=image)
markers = ndi.label(local_maxi)[0]
labels = watershed(-distance, markers, mask=image)

fig, axes = plt.subplots(ncols=3, figsize=(8, 2.7), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax0, ax1, ax2 = axes

ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('Overlapping objects')
ax1.imshow(-distance, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('Distances')
ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('Separated objects')

for ax in axes:
    ax.axis('off')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=0.9, bottom=0, left=0,
                    right=1)
plt.show()
