from datetime import date, timedelta
from core.models import db
from core.models.base_model import BaseModel, SlugModel

event_genres = db.Table(
    "event_genres",
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
)

class Event(SlugModel):
    __tablename__ = "events"
    date = db.Column(db.Date, nullable=False)
    ticket_link = db.Column(db.String(255), nullable=True)
    poster_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=True)
    poster = db.relationship("Media", backref='events')
    location = db.Column(db.String(150), nullable=False)
    short_desc = db.Column(db.Text, nullable=True)
    """  __mapper_args__ = {
        "order_by": date.asc()
    } """

    genres = db.relationship(
        "Genre",
        secondary=event_genres,
        backref=db.backref("events", lazy="dynamic"),
        lazy="dynamic"
    )

    @classmethod
    def get_for_month(cls, month: int, year: int):
        start = date(year, month, 1)

        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        return cls.query.filter(
            cls.date >= start,
            cls.date < end
        ).all()
    
    @classmethod
    def get_previous(cls, limit = None):
        query = cls.query.filter(cls.date < date.today()).order_by(cls.date.desc())
        if limit is not None:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_upcoming(cls, limit = None):
        query = cls.query.filter(cls.date >= date.today()).order_by(cls.date.asc())
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def has_passed(self):
        return self.date < date.today()

    @classmethod
    def get_home_gallery(cls):
        pass