upload_folder = "./uploads"

allowed_uploads = {
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "odt": "application/vnd.oasis.opendocument.text",
}
allowed_extensions = allowed_uploads.keys()
max_content_length = 16 * 1024 * 1024

# flask-uploads
UPLOADS_DEFAULT_DEST = upload_folder + "/project/static/img/"
UPLOADS_DEFAULT_URL = "http://localhost:5000/static/img/"

UPLOADED_IMAGES_DEST = upload_folder + "/project/static/img/"
UPLOADED_IMAGES_URL = "http://localhost:5000/static/img/"

allowed_mime_types = allowed_uploads.values()

static_path = "./static"
