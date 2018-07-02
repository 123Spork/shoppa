from flask import Flask
from flask_restful import Api
from shoppa.market.admin import AdminCreateProductView, AdminFetchProductView, AdminFetchAllProductsView, \
    AdminDestroyProductView, AdminUpdateProductView, AdminUpdateFeaturedProductsView, AdminFetchFeaturedProductsView
from shoppa.settings.admin import AdminConfigSettingsFetchView
from shoppa.settings.admin import AdminConfigSettingsUpdateView

app = Flask(__name__)
api = Api(app)

for resource in (
    AdminConfigSettingsUpdateView,
    AdminConfigSettingsFetchView,

    #products
    AdminCreateProductView,
    AdminFetchProductView,
    AdminFetchAllProductsView,
    AdminDestroyProductView,
    AdminUpdateProductView,

    #featured products
    AdminUpdateFeaturedProductsView,
    AdminFetchFeaturedProductsView

):
    api.add_resource(resource, resource.uri)

app.secret_key = "977d60c04eec1c62a98d1f534b2954fbwqepofnaofubf"
if __name__ == '__main__':
    app.run(debug=True)

