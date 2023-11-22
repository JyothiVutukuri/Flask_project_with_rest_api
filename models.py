from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False)

    def __init__(self, name, url):
        self.name = name.upper()
        self.url = url

    @classmethod
    def get_or_create(cls, name, url):
        site = cls.query.filter_by(name=name.upper()).first()
        if not site:
            site = cls(name=name, url=url)
            db.session.add(site)
            db.session.commit()
        return site


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()

    @classmethod
    def get_or_create(cls, name):
        brand = cls.query.filter_by(name=name.upper()).first()
        if not brand:
            brand = cls(name=name)
            db.session.add(brand)
            db.session.commit()
        return brand


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()

    @classmethod
    def get_or_create(cls, name):
        category = cls.query.filter_by(name=name.upper()).first()
        if not category:
            category = cls(name=name)
            db.session.add(category)
            db.session.commit()
        return category


class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.upper()

    @classmethod
    def get_or_create(cls, name):
        product_type = cls.query.filter_by(name=name.upper()).first()
        if not product_type:
            product_type = cls(name=name)
            db.session.add(product_type)
            db.session.commit()
        return product_type


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

    @classmethod
    def get_or_create(cls, name, price, page_number, site_id, brand_id, product_category_id, product_type_id):
        product = cls.query.filter_by(name=name.upper(), site_id=site_id).first()
        if not product:
            product = cls(
                name=name.upper(),
                price=price,
                page_number=page_number,
                site_id=site_id,
                brand_id=brand_id,
                product_category_id=product_category_id,
                product_type_id=product_type_id
            )
            db.session.add(product)
            db.session.commit()
        return product
