import logging
from sqlalchemy import Integer, String, Column

from shoppa.core.models import BaseSQLModel
from shoppa.market.managers import get_product_manager, get_featured_product_manager

log = logging.getLogger(__name__)

def get_product_class(category):
    table_name = "{0}_{1}".format(category, "product")

    if table_name in BaseSQLModel.registry:
        return BaseSQLModel.registry[table_name]
    else:
        class Product(BaseSQLModel):
            __tablename__ = table_name
            __table_args__ = {'useexisting': True}

            product_id = Column(Integer, primary_key=True)
            product_name = Column(String(200))
            product_description = Column(String(2048))
            product_cost = Column(Integer)

        Product.objects = get_product_manager(Product)()
        return Product


def get_featured_product_class():
    table_name = "featured_products"

    if table_name in BaseSQLModel.registry:
        return BaseSQLModel.registry[table_name]
    else:
        class FeaturedProduct(BaseSQLModel):
            __tablename__ = table_name
            __table_args__ = {'useexisting': True}

            featured_products_id = Column(String(100), primary_key=True)
            primary_product = Column(Integer)
            secondary_product_1 = Column(Integer)
            secondary_product_2 = Column(Integer)
            secondary_product_3 = Column(Integer)
            secondary_product_4 = Column(Integer)

        FeaturedProduct.objects = get_featured_product_manager(FeaturedProduct)()
        return FeaturedProduct