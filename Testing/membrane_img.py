### ndio membrane segmentation imports
import ndio
import ndio.remote.OCP as OCP
import ndio.remote.OCPMeta as NDLIMS
import ndio.convert.png as ndpng
import ndio.ramon.RAMONBase as ramonB
import ndio.ramon.RAMONVolume as ramonV
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

# Sets OCPQuery in Python
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

#membrane_query['token'] = 'kasthuri11cc'
#membrane_query['channel'] = 'image'
#membrane_query['resolution'] = 1

### Sets request URL
#service = '/ocp/ca'
#token = 'cv_kasthuri11_membrane_2014'
#channel = 'image'
#qobj = 11 #  imageDense = 11
#url = oo.url(suffix="/cv_kasthuri11_membrane_2014/image/hdf5/1/4400,5424/5440,6464/1100,1200/filter/11/")
# link = http://openconnecto.me/ocp/ca/cv_kasthuri11_membrane_2014/image/hdf5/1/4400,5424/5440,6464/1100,1200/filter/11/

#ramonV()

# Sets cutout arguments
membrane_images = oo.get_cutout(**membrane_query)

ndpng.export_png('membrane_pic2.png', membrane_images[0])
