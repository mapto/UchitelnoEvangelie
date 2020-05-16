#!/usr/bin/env python3

import os

from datetime import datetime
from urllib.parse import quote

from bottle import Bottle
from bottle import request, redirect, abort, static_file

from settings import allowed_extensions, allowed_mime_types
from settings import upload_folder, max_content_length, static_path

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

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    timestamped = datetime.now().strftime("%Y%m%d%H%M%S") + newfile.filename
    save_path = os.path.join(upload_folder, timestamped)
    newfile.save(save_path)

    # redirect to home page if it all works ok
    return redirect("/?" + quote("Файлът е качен!"))


@app.get("robots")
def root():
    return static_file("index.html", root=static_path)


@app.get("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /"


@app.get("/health")
def root():
    uploads = os.path.exists(upload_folder)
    if uploads:
        uploads = len([name for name in os.listdir(upload_folder)])
    return {"uploads": uploads if uploads else "absent"}


if __name__ == "__main__":
    app.run(debug=True, reloader=True)
