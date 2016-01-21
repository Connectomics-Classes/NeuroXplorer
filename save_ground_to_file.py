### ndio membrane segmentation imports
import ndio
import ndio.remote.OCP as OCP
import ndio.remote.OCPMeta as NDLIMS
import numpy as np

### Create OCP / OCPMeta objects
oo = OCP()
nn = NDLIMS()
###

print "Done importing packages"

image_token = 'kasthuri11cc'
annotation_token = 'kasthuri2015_ramon_v'
segmentation_token = 'ac3ac4'

# Get channel ROI for token
channel_ROI = nn.get_metadata(segmentation_token)['channels']

# Get membrane ROI coordinates
membrane_group_ROI = channel_ROI['ac4_neuron_truth']['rois']['ac4']

# Sets membrane query in Python
membrane_query = {
    'token': 'ac3ac4',
    'channel': 'ac4_neuron_truth',
    'x_start': membrane_group_ROI['x'][0],
    'x_stop': membrane_group_ROI['x'][1],
    'y_start': membrane_group_ROI['y'][0],
    'y_stop': membrane_group_ROI['y'][1],
    'z_start': membrane_group_ROI['z'][0],
    'z_stop': membrane_group_ROI['z'][1],
    'resolution': membrane_group_ROI['resolution'],
}

print "Getting images"
# Sets cutout arguments for ground truth membrane annotation
membrane_anno = oo.get_cutout(**membrane_query)

print "Printing to file"
np.save('nXp_ground.npy', membrane_anno)

print "Done."
