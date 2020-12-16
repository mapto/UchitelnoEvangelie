#!/usr/bin/env python3

import os

from datetime import datetime
from urllib.parse import quote
from zipfile import ZipFile

from bottle import Bottle  # type: ignore
from bottle import request, redirect, response, abort, error, static_file

from settings import allowed_extensions, allowed_mimetypes
from settings import upload_path, max_content_length, static_path

import exporter

app = Bottle(__name__)


def allowed_file(filename: str, file_mimetype: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
        and file_mimetype in allowed_mimetypes
    )


return_link = '<a href="/">Започнете отначало.</a>'


@error(404)
def mistake404(msg):
    response.content_type = "text/html"
    return "Несъществуваща страница: {}. {}".format(msg, return_link)


@error(405)
def mistake405(msg):
    response.content_type = "text/html"
    return "Непозволена заявка: {}. {}".format(msg, return_link)


@error(500)
def mistake500(msg):
    response.content_type = "text/html"
    return "Неочаквана грешка: {}. {}".format(msg, return_link)


@app.post("/upload")
def upload():
    """Handle file upload form"""

    # get the 'newfile' field from the form
    try:
        newfile = request.files.get("fileupload")
    except:
        abort(405, "Каченият файл не може да бъде прочетен")

    if not allowed_file(newfile.filename, newfile.content_type):
        abort(
            405,
            "Каченият файл не може да бъде разчетен. Поддържат се слените формати: {}".format(
                "|".join(allowed_extensions)
            ),
        )

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    xls_name = "{}-{}".format(ts, newfile.filename)
    save_path = os.path.join(upload_path, xls_name)
    newfile.save(save_path)

    exporter.read(save_path)

    # redirect to home page if it all works ok
    return redirect("/?f=" + quote(xls_name))


upload_ext_regex = ".+\.({})\.xlsx".format("|".join(allowed_extensions))


@app.get("/download/<url:re:" + upload_ext_regex + ">")
def download(url: str):
    return static_file(url, root=upload_path)


@app.get("/")
def root():
    return static_file("index.html", root=static_path)


@app.get("/dump")
def dump():
    fname = "dump.zip"

    full_path = os.path.join(static_path, fname)
    if os.path.exists(full_path):
        os.remove(full_path)

    with ZipFile(full_path, "w") as zipobj:
        for f in os.listdir(upload_path):
            zipobj.write(os.path.join(upload_path, f))

    return static_file(
        fname, root=static_path, mimetype="application/zip", download=True
    )


@app.get("/robots.txt")
def robots():
    response.content_type = "text/plain"
    return "User-agent: *\nDisallow: /"


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
