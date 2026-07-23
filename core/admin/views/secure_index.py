from flask_login import current_user
from flask_admin import  AdminIndexView, expose
from flask import  redirect, url_for, request

class SecuredAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('core.login', next=request.url))
        return super(SecuredAdminIndexView, self).index()