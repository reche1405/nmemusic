from core.models import db
from core.models.base_model import BaseModel
class Genre(BaseModel):
    __tablename__ = 'genres'
    title = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<Genre: {self.title}>"
    

