# How to grab our data and put it into a .npy file

# To load data in code:
#
# import numpy as np
#
# membrane_images = np.load('nXp_data.npy')
#

import ndio
import ndio.remote.OCP as OCP
oo = OCP()

import ndio.remote.OCPMeta as NDLIMS
nn = NDLIMS()

import ndio.convert.tiff as ndtiff	# For export to tiff later

import numpy as np

print "Done importing packages"

tokens = oo.get_public_tokens()

image_token = 'kasthuri11cc'
annotation_token = 'cv_kasthuri11_membrane_2014'

# Get channel ROI for token
channel_ROI = nn.get_metadata(annotation_token)['channels']

# Get membrane ROI coordinates
membrane_group_ROI = channel_ROI['image']['rois']['ac4']

# Sets membrane query in Python
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

print "Printing to file"
np.save('nXp_data.npy', membrane_images)

print "Done."
