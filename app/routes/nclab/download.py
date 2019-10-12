from flask import Blueprint, render_template, send_file
from pathlib import Path
from app import app

from app.models.nclab import Lectures, Documents, Attachments

api = Blueprint('/nclab', __name__)


@api.route('/document/<document_id>/attach/<file_id>', methods=["GET"])
def get_file(document_id, file_id):
    file = Attachments.query.filter_by(
        document_id=document_id,
        id=file_id).all()

    if len(file) is not 1:
        return 'Invalid Input', 404

    file_name = str(Path.cwd() / 'upload' / file[0].filename)

    return send_file(file_name, mimetype=None, attachment_filename=file[0].filename, as_attachment=True)


@api.route('/attach/<file_id>', methods=["GET"])
def get_file_by_id(file_id):
    file = Attachments.query.filter_by(id=file_id).all()

    if len(file) is not 1:
        return 'Invalid Input', 404

    file_name = str(Path.cwd() / 'upload' / file[0].filename)

    return send_file(file_name, mimetype=None, attachment_filename=file[0].filename, as_attachment=True)


app.register_blueprint(api, url_prefix='/nclab')
