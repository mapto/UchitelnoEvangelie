import os

curdir = os.path.dirname(os.path.realpath(__file__))
os.path.curdir = curdir

upload_path = os.path.join(curdir, "uploads")

allowed_uploads = {
    # "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # "odt": "application/vnd.oasis.opendocument.text",
}
allowed_extensions = allowed_uploads.keys()
max_content_length = 16 * 1024 * 1024

allowed_mimetypes = allowed_uploads.values()

static_path = os.path.join(curdir, "static")
