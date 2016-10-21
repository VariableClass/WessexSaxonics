# [START imports]
import sys
sys.path.append('lib')

import os
import cloudstorage as gcs

# [END imports]

from google.appengine.api import app_identity, users


# Upload image to cloud storage bucket
def upload_image_file(image, name, image_type):

    # Define retry parameters
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)

    # Retrieve default bucket
    bucket_name = _retrieve_default_bucket()

    # Define filename
    filename = '/' + bucket_name + '/' + name

    # Create new cloud storage file to write to
    gcs_file = gcs.open(filename, 'w', content_type=image_type, retry_params=write_retry_params)

    # Write the image file to cloud storage
    gcs_file.write(image)

    # Close the cloud storage file
    gcs_file.close()

    # Store URL to return image
    gcs_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket': bucket_name, 'file': name}

    return gcs_url


# Retrieve image from cloud storage bucket
def retrieve_image_file(filename):

    # Retrieve default bucket
    bucket_name = _retrieve_default_bucket()

    # Open image file from cloud storage to read from
    gcs_file = gcs.open('/' + bucket_name + '/' + filename)

    # Read image file from cloud storage
    image = gcs_file.read()

    # Close the cloud storage file
    gcs_file.close()

    return image


# Retrieve default bucket
def _retrieve_default_bucket():

    # Retrieve default bucket
    return os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
