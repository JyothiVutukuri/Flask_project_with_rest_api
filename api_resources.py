from flask_restful import Resource
from flask import jsonify
from models import Site, Brand, Product, ProductCategory, ProductType


class SiteResource(Resource):
    def get(self):
        sites = Site.query.all()
        return jsonify({'sites': [{'id': site.id, 'name': site.name, 'url': site.url} for site in sites]})


class BrandResource(Resource):
    def get(self):
        brands = Brand.query.all()
        return jsonify({'brands': [{'id': brand.id, 'name': brand.name} for brand in brands]})


class CategoryResource(Resource):
    def get(self):
        categories = ProductCategory.query.all()
        return jsonify({'categories': [{'id': category.id, 'name': category.name} for category in categories]})


class TypeResource(Resource):
    def get(self):
        types = ProductType.query.all()
        return jsonify({'product_types': [{'id': type.id, 'name': type.name} for type in types]})


class ProductResource(Resource):
    def get(self, brand_id):
        products = Product.query.filter_by(brand_id=brand_id).all()
        return jsonify(
            {'products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'page_number': product.page_number,
                    'site': product.site.name,
                    'brand': product.brand.name,
                    'product_category': product.product_category.name,
                    'product_type': product.product_type.name if product.product_type else None
                } for product in products]
            }
        )


class ProductDetailResource(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if product:
            return jsonify({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'page_number': product.page_number,
                'site': {'id': product.site.id, 'name': product.site.name, 'url': product.site.url},
                'brand': {'id': product.brand.id, 'name': product.brand.name},
                'product_category': {'id': product.product_category.id, 'name': product.product_category.name},
                'product_type': {'id': product.product_type.id,
                                 'name': product.product_type.name} if product.product_type else None
            })
        else:
            return jsonify({'message': 'Product not found'}), 404
