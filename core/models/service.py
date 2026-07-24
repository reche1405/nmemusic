from core.models import db
from core.models.base_model import SlugModel

class Service(SlugModel):
    __tablename__ = 'services'
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text, nullable=False)
    featured_media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref='service_feature')

    def __repr__(self):
        return f"<Service: {self.title}>"

