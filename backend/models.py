from google.appengine.ext import blobstore, ndb
from google.appengine.api import images


class Image(ndb.Model):
    name = ndb.StringProperty()
    user_id = ndb.StringProperty()
    height = ndb.IntegerProperty()
    width = ndb.IntegerProperty()
    bucket_name = ndb.StringProperty()

    # Retrieve public URL for image
    @property
    def public_url(self):

        if self.bucket_name is None or self.name is None:
            return None

        else:

            # Build blobstore type filename
            blobstore_filename = '/gs/' + self.bucket_name + '/' + self.name

            # Get blobstore key
            key = blobstore.create_gs_key(blobstore_filename)

            # Return scaled image serving URL
            return images.get_serving_url(key)

    @property
    def thumbnail(self):

        if self.bucket_name is None or self.name is None:
            return None

        else:

            # Build blobstore type filename
            blobstore_filename = '/gs/' + self.bucket_name + '/' + self.name

            # Get blobstore key
            key = blobstore.create_gs_key(blobstore_filename)

            # Return scaled image serving URL
            return images.get_serving_url(key, size=128)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query(cls.user_id == user_id)

    @classmethod
    def get_image_by_user(cls, name, user_id):
        return cls.query(cls.user_id == user_id, cls.name == name).get()

    @classmethod
    def delete_user_image(cls, name, user_id):
        key = cls.get_image_by_user(name, user_id).key
        key.delete()