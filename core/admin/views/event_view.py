import io, os
from flask import flash, current_app
from zipfile import ZipFile
from slugify import slugify
from .base_sceure_veiw import BaseSecureView
from wtforms.validators import Optional
from wtforms.fields import FileField
from werkzeug.utils import secure_filename
from core.models import db
from core.models.media import Media
from core.models.gallery import Gallery, Slide
from PIL import ImageOps, Image
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

class EventAdminView(BaseSecureView):
    """Admin view for Project with inline Units in the form."""
    # Show units inline on the project edit/create form
    form_columns = ['title', 'short_desc',  'date', 'zip_file', 'location']
    column_list = ['title', 'short_desc', 'date']
    
    form_extra_fields = {
        'zip_file': FileField('Bulk Upload Images (.zip)', validators=[Optional()])
    }
    # Optionally auto-generate slug from project title
    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if getattr(model, 'title', None):
            base_slug  = slugify(model.title)
            counter = 1
            slug = base_slug
        # Loop to ensure uniqueness against existing slugs
        while Media.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        model.slug = slug    

        if form.zip_file.data:
            zip_file_storage = form.zip_file.data
            
            if zip_file_storage.filename.endswith('.zip'):
                try:
                    # 1. Process zip and get the list of created Media objects
                    new_media_items = process_zip_upload(zip_file_storage)
                    
                    if new_media_items:
                        # 2. Append to the many-to-many relationship
                        # 'media' is the relationship attribute on your Project model
                        gallery = None
                        start_index = 0
                        if model.gallery:
                            gallery = model.gallery
                            start_index = len(gallery.slides) + 1
                        else:
                            gallery = Gallery(
                                name=model.title,
                                event_id=model.id,
                            )
                            db.session.add(gallery)
                            db.session.flush()
                        slides = generate_slides(new_media_items, gallery.id, start_index)

                        # Inform the admin user of success
                        flash(f'Successfully extracted and linked {len(new_media_items)} images.', 'success')
                    else:
                        flash('Zip file parsed, but no valid images were found.', 'warning')
                        
                except Exception as e:
                    # Flask-Admin handles exceptions gracefully, but dropping a flash helps
                    flash(f'Error processing zip file: {str(e)}', 'error')
                    raise e # Raising the exception rolls back the DB transaction automatically
            else:
                flash('Uploaded file was not a valid ZIP archive.', 'error')
       


def process_zip_upload( zip_file_storage):
    """
    Takes a FileStorage object (from request.files), extracts images,
    saves them, and returns a list of created Media objects.
    """
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1920
    IMAGE_QUALITY = 95 # 80-85 is the sweet spot for web optimization
    media_objects = []
    
    # Read the zip file into memory
    zip_data = io.BytesIO(zip_file_storage.read())
    upload_path = current_app.config['UPLOAD_PATH']
    
    with ZipFile(zip_data, 'r') as archive:
        for file_info in archive.infolist():
            # Skip directories and hidden system files (like __MACOSX)
            if file_info.is_dir() or file_info.filename.startswith('__'):
                continue
                
            raw_filename = os.path.basename(file_info.filename)
            if raw_filename and allowed_file(raw_filename):
                secure_name = secure_filename(raw_filename)
                
                # Extract the file data as bytes
                #file_bytes = archive.read(file_info.filename)
                
                # --- YOUR EXISTING STORAGE LOGIC HERE ---


                # Example: If you save to a local folder:
                filepath = os.path.join(upload_path, secure_name)
                """ with open(filepath, 'wb') as f:
                    f.write(file_bytes) """
                # ----------------------------------------
                cleaned_name = secure_filename(raw_filename)
                name_without_ext, ext = os.path.splitext(cleaned_name)
                
                # 2. Derive fields
                # Replace dashes/underscores with spaces for a clean title
                title = name_without_ext.replace('-', ' ').replace('_', ' ').title()
                alt_tag = f"Image showing {title}"
                slug = generate_unique_slug(name_without_ext)
            
                # 3. Define and handle paths
                # To prevent filename collisions on disk, you can append the slug to the filename
                final_filename = f"{cleaned_name}"
                relative_path = f'{final_filename}'
                absolute_path = filepath
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

                # --- PILLOW PROCESSING LOGIC ---
                # 1. Read bytes from zip into a stream
                file_bytes = archive.read(file_info.filename)
                image_stream = io.BytesIO(file_bytes)
                
                with Image.open(image_stream) as img:
                    # Fix orientation (Smartphones often save orientation metadata instead of rotating pixels)
                    img = ImageOps.exif_transpose(img)
                    
                    # Convert to RGB if it's RGBA (PNG) so it can save as a JPEG smoothly
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 2. Resize proportionally if it exceeds maximum boundaries
                    img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
                    
                    # 3. Save directly to disk with optimization parameters
                    img.save(absolute_path, optimize=True, quality=IMAGE_QUALITY)
                # -------------------------------
                
                media_item = Media(
                    title=title,
                    filename=final_filename,
                    relative_path=relative_path,
                    alt_tag=alt_tag,
                    slug=slug,
                    description=f"Bulk uploaded via zip archive: {zip_file_storage.filename}"
                )
                
                db.session.add(media_item)
                media_objects.append(media_item)
                
    return media_objects

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def generate_unique_slug( base_title):
    """Generates a clean, unique slug by checking the database."""
    base_slug = slugify(base_title)
    if not base_slug:
        base_slug = "media-file"
        
    slug = base_slug
    counter = 1
    
    # Loop to ensure uniqueness against existing slugs
    while Media.query.filter_by(slug=slug).first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    return slug

def generate_slides(media, gallery_id, start_index = 0):
    slides = []
    sort_order = start_index
    for item in media:
        slide = Slide(
            gallery_id = gallery_id,
            sort_order = sort_order,
            media_id = item.id
        )
        db.session.add(slide)
        slides.append(slide)
        sort_order += 1
    return slides
 