from flask_admin.form import FileUploadField, FileUploadInput
from markupsafe import Markup

# 1. Keep the custom widget as it was

class ImagePreviewWidget(FileUploadInput):
    def __call__(self, field, **kwargs):
        html = super(ImagePreviewWidget, self).__call__(field, **kwargs)
        if field.data:
            # Adjust "/static/uploads/" to your setup
            preview_html = f'<div style="margin-bottom: 10px;"><img src="/media/{field.data}" style="max-height: 150px; border: 1px solid #ddd; padding: 5px; border-radius: 4px;"></div>'
            html = Markup(preview_html) + html
        return html

# 2. Define a custom field that uses your widget by default
class PreviewFileUploadField(FileUploadField):
    widget = ImagePreviewWidget()