### ndio membrane segmentation imports
import ndio
import ndio.remote.OCP as OCP
import ndio.remote.OCPMeta as NDLIMS
import ndio.convert.tiff as ndtiff
###

### Create OCP / OCPMeta objects
oo = OCP()
nn = NDLIMS()
###

# Get all tokens
tokens = oo.get_public_tokens()

# Membrane group image and annotation tokens for membrane image in datamap
image_token = 'kasthuri11cc'
annotation_token = 'cv_kasthuri11_membrane_2014'

# Get channel ROI for token
channel_ROI = nn.get_metadata('cv_kasthuri11_membrane_2014')['channels']

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

# Sets cutout arguments
membrane_images = oo.get_cutout(**membrane_query)

ndtiff.export_tiff('membrane_pic1.tiff', membrane_images[0])
