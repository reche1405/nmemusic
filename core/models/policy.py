from core.models import db
from core.models.base_model import SlugModel
class Policy(SlugModel):
    __tablename__="policies"
    url_prefix = 'policies'
    parent_route = db.Column(db.String(255), nullable=False, default='policy_list')
    parent_title = db.Column(db.String(255), nullable=False, default='Legal Stuff')
    intro = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)

    






