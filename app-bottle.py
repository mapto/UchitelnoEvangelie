#!/usr/bin/env python3

import os

from datetime import datetime
from urllib.parse import quote

from bottle import Bottle
from bottle import request, redirect, abort, static_file

from settings import allowed_extensions, allowed_mime_types
from settings import upload_path, max_content_length, static_path

app = Bottle(__name__)


def allowed_file(filename: str, file_mime_type: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
        and file_mime_type in allowed_mime_types
    )


@app.post("/")
def upload():
    """Handle file upload form"""

    # get the 'newfile' field from the form
    try:
        newfile = request.files.get("fileupload")
    except:
        return redirect("/?" + quote("Неочаквана грешка"))

    if not allowed_file(newfile.filename, newfile.content_type):
        return redirect("/?" + quote("Файлът не може да бъде разчетен"))

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    save_path = os.path.join(upload_path, "{}-{}".format(ts, newfile.filename))
    newfile.save(save_path)

    # redirect to home page if it all works ok
    return redirect("/?" + quote("Файлът е качен!"))


@app.get("/")
def root():
    return static_file("index.html", root=static_path)


@app.get("/robots.txt")
def robots():
    return "User-agent: *<br/>Disallow: /"


@app.get("/healthcheck")
def healthcheck():
    uploads = os.path.exists(upload_path)
    if uploads:
        uploads = len(os.listdir(upload_path))

    static = os.path.exists(static_path)
    if static:
        static = len(os.listdir(static_path))

    return {
        "uploads": {"path": upload_path, "files": uploads if uploads else "absent"},
        "static": {"path": static_path, "files": static if static else "absent"},
    }


if __name__ == "__main__":
    app.run(debug=True, reloader=True)
