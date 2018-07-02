from shoppa.core.managers import CoreSQLDBModelManager


def get_product_manager(model):

    class ProductManager(CoreSQLDBModelManager):
        Model = model
    return ProductManager


def get_featured_product_manager(model):

    class FeaturedProductManager(CoreSQLDBModelManager):
        Model = model
    return FeaturedProductManager