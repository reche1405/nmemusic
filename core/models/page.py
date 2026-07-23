from core.models import db
from core.models.base_model import BaseModel
from enum import Enum

class HeroHeight(Enum):
    NA = "height__none"
    SM = "height__small"
    LG = "height__large"

    def __str__(self):
        return self.value

class Page(BaseModel):
    __tablename__ = "pages"
    title = db.Column(db.String(100), nullable=False)
    keywords = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    hero_size = db.Column(db.Enum(HeroHeight, native_enum=False), default=HeroHeight.SM, nullable=False)
    hero_media_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=True)
    hero_media = db.relationship('Media', backref="heroes")
    tag = db.Column(db.String(100), nullable=False)

    @classmethod
    def get_for_tag(cls, tag):
        return cls.query.filter_by(tag=tag).first()
    
    def section(self, tag):
        return next((s for s in self.sections if s.tag == tag), None)


class Section(BaseModel):
    __tablename__ = "sections"
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"), nullable=False)
    page = db.relationship('Page', backref="sections")
    title = db.Column(db.String(200), nullable=True)
    subtitle = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=True)
    cta_link = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.String(100), nullable=False)

    


  