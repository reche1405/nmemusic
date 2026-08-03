from core.models import db
from core.models.base_model import SlugModel, BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    title = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f"<Category: {self.title}>"

    def get_members(self):
        return self.services

    @classmethod
    def get_group(cls, group_name='primary'):
        return cls.query.filter_by(title=group_name).first()


class Service(SlugModel):
    __tablename__ = 'services'
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text, nullable=False)
    featured_media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref='service_feature')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='services')

    def __repr__(self):
        return f"<Service: {self.title}>"

