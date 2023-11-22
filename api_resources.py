from flask_restful import Resource, abort
from flask import jsonify, request
from models import Site, Brand, Product, ProductCategory, ProductType


def get_paginated_list(results, url, start, limit, page_number):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    obj['page_number'] = page_number  # Include the current page number
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


class PaginatedResourceBase(Resource):
    def get_paginated_response(self, results):
        url = request.base_url
        start = request.args.get('start', 1)
        limit = request.args.get('limit', 20)
        page_number = (int(start) - 1) // int(limit) + 1  # Calculate the current page number
        return jsonify(get_paginated_list(results, url, start, limit, page_number))


class SiteResource(PaginatedResourceBase):
    def get(self):
        sites = Site.query.all()
        data = [{'id': site.id, 'name': site.name, 'url': site.url} for site in sites]
        return self.get_paginated_response(data)


class BrandResource(PaginatedResourceBase):
    def get(self):
        brands = Brand.query.all()
        data = [{'id': brand.id, 'name': brand.name} for brand in brands]
        return self.get_paginated_response(data)


class CategoryResource(PaginatedResourceBase):
    def get(self):
        categories = ProductCategory.query.all()
        data = [{'id': category.id, 'name': category.name} for category in categories]
        return self.get_paginated_response(data)


class TypeResource(PaginatedResourceBase):
    def get(self):
        types = ProductType.query.all()
        data = [{'id': type.id, 'name': type.name} for type in types]
        return self.get_paginated_response(data)


class ProductListResource(PaginatedResourceBase):
    def get(self, brand_id):
        products = Product.query.filter_by(brand_id=brand_id).all()
        data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'page_number': product.page_number,
                'site': product.site.name,
                'brand': product.brand.name,
                'product_category': product.product_category.name,
                'product_type': product.product_type.name if product.product_type else None
            } for product in products
        ]
        return self.get_paginated_response(data)


class ProductListBySiteResource(PaginatedResourceBase):
    def get(self, site_id):
        products = Product.query.filter_by(site_id=site_id).all()

        data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'page_number': product.page_number,
                'site': product.site.name,
                'brand': product.brand.name,
                'product_category': product.product_category.name,
                'product_type': product.product_type.name if product.product_type else None
            } for product in products
        ]
        return self.get_paginated_response(data)


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
