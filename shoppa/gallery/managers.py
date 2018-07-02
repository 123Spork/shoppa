from shoppa.core.managers import CoreSQLDBModelManager

def get_image_resource_manager(model):

    class ImageResourceManager(CoreSQLDBModelManager):
        Model = model
    return ImageResourceManager