import os, io
from werkzeug.utils import secure_filename
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineFormAdmin 
from flask_login import current_user
from flask_admin import form, AdminIndexView, expose
from flask import current_app, redirect, url_for, request, flash
from core.models import db
from slugify import slugify

from wtforms.fields import FileField
from wtforms.validators import Optional
from zipfile import ZipFile


class BaseSecureView(ModelView):
    form_excluded_columns = ['created_at' ,'updated_at']
    def is_accessible(self):
        # Only allow access if the user is authenticated
        # Pro tip: If your User model has an 'is_admin' field, check it here: 
        # return current_user.is_authenticated and current_user.is_admin
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect logged-out users straight to your custom login view.
        # request.url ensures the user is sent back here after typing their password.

        return redirect(url_for('core.login', next=request.url))
    
class SlugModelView(BaseSecureView):
    form_excluded_columns = ['created_at', 'updated_at', 'slug']

    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super().on_model_change(form, model, is_created)