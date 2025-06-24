from flask import Blueprint, request, url_for, jsonify, redirect, current_app
from helpers import get_secure_filename_filepath, download_from_s3
from PIL import Image, ImageFilter, ImageEnhance
import os

bp = Blueprint("filters", __name__, url_prefix="/filters")


@bp.route("/blur", methods=["POST"])
def blur():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        radius = int(request.json["radius"])  # type: ignore
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.filter(ImageFilter.GaussianBlur(radius))
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found "}), 404


@bp.route("/contrast", methods=["POST"])
def contrast():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        factor = float(request.json["factor"])  # type: ignore
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = ImageEnhance.Contrast(image).enhance(factor)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found "}), 404


@bp.route("/brightness", methods=["POST"])
def brightness():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)
    try:
        factor = float(request.json["factor"])  # type: ignore
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = ImageEnhance.Brightness(image).enhance(factor)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found "}), 404
