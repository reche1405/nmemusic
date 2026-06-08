from core.models import db
import datetime
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now )
    updated_at = db.Column('last_updated', db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    

