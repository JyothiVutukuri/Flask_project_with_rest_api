from app import app
from models import db, Site


def create_tables():
    db.create_all()


def add_site_data(name, url):
    with app.app_context():
        site = Site.query.filter_by(name=name.upper()).first()
        if site:
            return

        new_site = Site(name=name, url=url)
        db.session.add(new_site)
        db.session.commit()


# Add specific data here
if __name__ == '__main__':
    with app.app_context():
        create_tables()

    add_site_data(name='zeigns', url='https://zeigns.nl')
    add_site_data(name='zalando', url='https://zalando.nl')
    add_site_data(name='omoda', url='https://omoda.nl')