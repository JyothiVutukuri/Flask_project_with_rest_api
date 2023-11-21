# apps.py
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api

from api_resources import SiteResource, BrandResource, ProductResource, ProductDetailResource, CategoryResource, TypeResource
from models import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indexed_data.db'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return render_template('home.html')


# Indexed websites info
api.add_resource(SiteResource, '/api/sites')
api.add_resource(BrandResource, '/api/brands')
api.add_resource(CategoryResource, '/api/categories')
api.add_resource(TypeResource, '/api/product_types')
api.add_resource(ProductResource, '/api/brands/<int:brand_id>/products')
api.add_resource(ProductDetailResource, '/api/products/<int:product_id>')


if __name__ == '__main__':
    # You can choose to add specific data here if needed
    app.run(debug=True)
