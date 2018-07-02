from sqlalchemy import Integer, String, Column

from shoppa.core.models import BaseSQLModel
from shoppa.gallery.managers import get_image_resource_manager

def get_image_resource_class():
    table_name = "{0}".format("resouce")

    if table_name in BaseSQLModel.registry:
        return BaseSQLModel.registry[table_name]
    else:
        class AnalyticsEventSQLStore(BaseSQLModel):
            __tablename__ = table_name
            __table_args__ = {'useexisting': True}

            image_id = Column(Integer, primary_key=True, autoincrement=True)
            image_name = Column(String)
            image_url = Column(String)

            """def upload_image_from_data(self, key=None, image_data=None):
            storage = getattr(settings, "IMAGE_RESOURCE_STORAGE", None)
            if storage and key and image_data and self.object_id:
                remote_file_name = "{0}_{1}.{2}".format(
                    self.object_id,
                    binascii.hexlify(os.urandom(randint(24, 32))).decode(),
                    image_data['file_extension'])
                self.image_urls[key] = CDNAdapter.upload_base_64_encoded_data(
                    remote_file_name=remote_file_name,
                    base_64_encoded_data=image_data['image'], bucket_name=storage['bucket'],
                    cdn_location=storage['cdn_location'])
                self.save()"""

        AnalyticsEventSQLStore.objects = get_image_resource_manager(AnalyticsEventSQLStore)()

