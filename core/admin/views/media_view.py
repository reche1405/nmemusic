from .base_sceure_veiw import BaseSecureView
from core.admin.forms.media import PreviewFileUploadField
from zipfile import ZipFile
import os, io
from werkzeug.utils import secure_filename
from slugify import slugify

from flask import current_app
class MediaAdminView(BaseSecureView):

    def __init__(self, model, session, *args, **kwargs):
        self.form_args = {
            'relative_path': {
                'label': 'Upload Media File',
                'base_path': current_app.config['UPLOAD_PATH'], # Dynamic import!
                'allow_overwrite': False,
            }
        }
        super(MediaAdminView, self).__init__(model, session, *args, **kwargs)
    # 1. Show the path and slug in the dashboard table list
    column_list = ['id', 'title', 'filename', 'slug', 'relative_path']

    # 2. Tell Flask-Admin to render a file upload input instead of a text field
    form_overrides = {
        'relative_path': PreviewFileUploadField
    }

    def on_model_change(self, form, model, is_created):
        """
        SQLAlchemy Hook: This intercepts the form data right before it saves 
        to the database, allowing us to auto-populate the filename and slug.
        """
        if model.relative_path:
            # Flask-Admin's FileUploadField automatically saves the file to disk
            # and updates model.relative_path to just the filename (e.g., "roof_damage.jpg").
            
            # 1. Clean and store the filename safely
            model.filename = secure_filename(model.relative_path)
            
            # 2. Auto-generate the unique slug from the filename (removing extension)
            name_without_ext = os.path.splitext(model.filename)[0]
            
            model.slug = slugify(name_without_ext)
