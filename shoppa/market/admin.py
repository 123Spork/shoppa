import json

from flask import Response
from shoppa.core.exceptions import ObjectNotFound
from shoppa.core.http import crossdomain, parse_args, request_data
from shoppa.core.views import BaseAdminView
from shoppa.market.models import get_product_class, get_featured_product_class


class AdminCreateProductView(BaseAdminView):
    """
        URI: /admin/products/create
        POST: Create a product.
    """
    uri = '/admin/products/create'

    @crossdomain(origin='*')
    #@requires_admin_login
    def post(self):
        try:
            args = parse_args(
                (
                    ('product_name', str, True),
                    ('product_description', str, True),
                    ('product_cost', float, True),
                ),request_data())
        except Exception as e:
            return Response(status=400, response=json.dumps({
                'session_id': self.user.session_id,
                'error_message': "Server received invalid arguments. Expecting product_name, product_description and product_cost.",
                'error_location': '/admin/products/create POST'
            }))

        ProductClass = get_product_class("blank")
        product = ProductClass(
            product_name = args['product_name'],
            product_description = args['product_description'],
            product_cost = args['product_cost']
        )
        product.save()

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'product': product.to_dict()
            }))

class AdminFetchAllProductsView(BaseAdminView):
    """
        URI: /admin/products/fetch
        POST: Fetch all products.
    """
    uri = '/admin/products/fetch'

    @crossdomain(origin='*')
    #@requires_admin_login
    def get(self):
        try:
            ProductClass = get_product_class("blank")
            products = ProductClass.objects.get_multi()
        except ObjectNotFound:
            return Response(status=404, response=json.dumps({
                #'session_id': self.user.session_id,
                'error_message': "No products found",
                'error_location': '/admin/products/fetch GET'
            }))

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'products': [product.to_dict() for product in products]
            }))


class AdminFetchProductView(BaseAdminView):
    """
        URI: /admin/products/<string:product_id>/fetch
        POST: Fetch a product.
    """
    uri = '/admin/products/<string:product_id>/fetch'

    @crossdomain(origin='*')
    #@requires_admin_login
    def get(self, product_id):
        try:
            ProductClass = get_product_class("blank")
            product = ProductClass.objects.get(
                product_id=product_id
            )
        except ObjectNotFound:
            return Response(status=404, response=json.dumps({
                #'session_id': self.user.session_id,
                'error_message': "No products found with id: {0}".format(product_id),
                'error_location': '/admin/products/{0}/update POST'.format(product_id)
            }))

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'product': product.to_dict()
            }))



class AdminUpdateProductView(BaseAdminView):
    """
        URI: /admin/products/<string:product_id>/update
        POST: Update a product.
    """
    uri = '/admin/products/<string:product_id>/update'

    @crossdomain(origin='*')
    #@requires_admin_login
    def post(self, product_id):
        try:
            args = parse_args(
                (
                    ('product_name', str, True),
                    ('product_description', str, True),
                    ('product_cost', float, True),
                ),request_data())
        except Exception as e:
            return Response(status=400, response=json.dumps({
                #'session_id': self.user.session_id,
                'error_message': "Server received invalid arguments. Expecting product_name, product_description and product_cost.",
                'error_location': '/admin/products/create POST'
            }))

        try:
            ProductClass = get_product_class("blank")
            product = ProductClass.objects.get(
                product_id=product_id
            )
        except ObjectNotFound:
            return Response(status=404, response=json.dumps({
                #'session_id': self.user.session_id,
                'error_message': "No products found with id: {0}".format(product_id),
                'error_location': '/admin/products/{0}/update POST'.format(product_id)
            }))

        product.product_name = args['product_name']
        product.product_description = args['product_description']
        product.product_cost = args['product_cost']
        product.save()

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'product': product.to_dict()
            }))


class AdminDestroyProductView(BaseAdminView):
    """
        URI: /admin/products/<string:id>/delete
        POST: Delete a product.
    """
    uri = '/admin/products/<string:product_id>/delete'

    @crossdomain(origin='*')
    #@requires_admin_login
    def post(self, product_id):

        try:
            ProductClass = get_product_class("blank")
            product = ProductClass.objects.get(
                product_id=product_id
            )
        except ObjectNotFound:
            return Response(status=404, response=json.dumps({
                #'session_id': self.user.session_id,
                'error_message': "No products found with id: {0}".format(product_id),
                'error_location': '/admin/products/{0}/delete POST'.format(product_id)
            }))
        product.delete()

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'success': True
            }))


class AdminUpdateFeaturedProductsView(BaseAdminView):
    """
        URI: /admin/settings-config/update
        POST: Update featured products
    """
    uri = '/admin/featured-products/update'

    @crossdomain(origin='*')
    #@requires_admin_login
    def post(self):
        try:
            args = parse_args(
                (
                    ('primary_product', int, True),
                    ('secondary_product_1', int, True),
                    ('secondary_product_2', int, True),
                    ('secondary_product_3', int, True),
                    ('secondary_product_4', int, True),
                ),request_data())
        except Exception as e:
            return Response(status=400, response=json.dumps({
                'error_message': "Server received invalid arguments. Expecting primary_product, secondary_product_1\
                    secondary_product_2, secondary_product_3 and secondary_product_4",
                'error_location': '/admin/featured-products/update POST'
            }))

        FeaturedProductClass = get_featured_product_class()
        try:
            featured_products = FeaturedProductClass.objects.get(
                featured_products_id="base"
            )
        except ObjectNotFound:
            featured_products = FeaturedProductClass(
                featured_products_id="base",
                primary_product=args['primary_product'],
                secondary_product_1=args['secondary_product_1'],
                secondary_product_2=args['secondary_product_2'],
                secondary_product_3=args['secondary_product_3'],
                secondary_product_4=args['secondary_product_4'],
            )
            featured_products.save()
        else:
            featured_products.site_name=args['site_name']
            featured_products.primary_product=args['primary_product']
            featured_products.secondary_product_1=args['secondary_product_1']
            featured_products.secondary_product_2=args['secondary_product_2']
            featured_products.secondary_product_3=args['secondary_product_3']
            featured_products.secondary_product_4=args['secondary_product_4']
            featured_products.save()

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'featured_products': featured_products.to_dict()
            }))


class AdminFetchFeaturedProductsView(BaseAdminView):
    """
        URI: /admin/featured-products/fetch
        POST: Fetch all featured products.
    """
    uri = '/admin/featured-products/fetch'

    @crossdomain(origin='*')
    #@requires_admin_login
    def get(self):

        FeaturedProductClass = get_featured_product_class()
        try:
            featured_products = FeaturedProductClass.objects.get(
                featured_products_id="base"
            )
        except ObjectNotFound:
            featured_products = FeaturedProductClass(
                settings_id="base",
                primary_product=None,
                secondary_product_1=None,
                secondary_product_2=None,
                secondary_product_3=None,
                secondary_product_4=None
            )

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'featured_products': featured_products.to_dict()
            }))