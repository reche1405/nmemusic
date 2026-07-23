from datetime import datetime
import enum
from core.models import db
from sqlalchemy.ext.orderinglist import ordering_list

class Orientation(enum.Enum):
    Portrait = "portrait"
    Landscape = 'landscape'
    def __str__(self):
        return self.value

class Gallery(db.Model):
    __tablename__ = 'galleries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='Default Slideshow')
    orientation = db.Column(db.Enum(Orientation), default=Orientation.Portrait, nullable=False)
    
    # Foreign Key & Relationship to Project
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete="CASCADE"), unique=True, nullable=True)
    event = db.relationship('Event', backref=db.backref('gallery', uselist=False, lazy=True))


    slides = db.relationship(
        'Slide', 
        order_by='Slide.sort_order', 
        collection_class=ordering_list('sort_order'),
        cascade="all, delete-orphan",
        backref='gallery'
    )

    def __repr__(self):
        return f"<Gallery {self.name} (Event ID: {self.event_id})>"
    
    def to_json(self):
        json = {
            "items" : [slide.to_json() for slide in self.slides],
            'orientation' : 'horizontal',
            'autoplay_interval': 4000  # or get from project settings
        }
        json['event_title'] = self.event.title if self.event else "Home Gallery"

        json['event_id'] = self.event.id if self.event else 0
        return json
    


class Slide(db.Model):
    __tablename__ = 'slides'
    
    id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.id', ondelete="CASCADE"), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0) # Made non-nullable for ordering_list
    
    # Relationship to Media
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
    # Changed backref to 'slides' (plural) to avoid naming collisions if Media is used elsewhere
    media = db.relationship('Media', backref=db.backref('slides', lazy=True))
    
    def __repr__(self):
        return f"<Slide id={self.id} gallery_id={self.gallery_id} order={self.sort_order}>"
    
    def to_json(self):
        return self.media.to_carousel_dict()

