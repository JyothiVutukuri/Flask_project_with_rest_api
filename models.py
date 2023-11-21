from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False)

    def __init__(self, name, url):
        self.name = name.upper()
        self.url = url


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()


class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=True)
    page_number = db.Column(db.Integer, nullable=True)

    # Foreign key relationships
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=True)

    # Relationships with backref
    site = db.relationship('Site', backref='products')
    brand = db.relationship('Brand', backref='products')
    product_category = db.relationship('ProductCategory', backref='products')
    product_type = db.relationship('ProductType', backref='products')

    __table_args__ = (
        db.UniqueConstraint('name', 'site_id', name='unique_product_name_site_id'),
    )

    def __init__(self, name, price, page_number, site_id, brand_id, product_category_id, product_type_id):
        self.name = name.upper()
        self.price = price
        self.page_number = page_number
        self.site_id = site_id
        self.brand_id = brand_id
        self.product_category_id = product_category_id
        self.product_type_id = product_type_id
