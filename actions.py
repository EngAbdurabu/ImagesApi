from flask import Blueprint, request, redirect, url_for, jsonify, current_app
from helpers import get_secure_filename_filepath, download_from_s3
from PIL import Image
import os

bp = Blueprint("actions", __name__, url_prefix="/actions")


@bp.route("/resize", methods=["POST"])
def resize():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        width, height = int(request.json["width"]), int(request.json["height"])  # type: ignore
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.resize((width, height))
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404


@bp.route("/preset/<preset>", methods=["POST"])
def resizer_preset(preset):
    presets = {"small": (640, 480), "medium": (1280, 960), "large": (1600, 1200)}
    if preset not in presets:
        return jsonify({"message": "The preset is not available "}), 400

    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        size = presets[preset]
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.resize(size)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404


@bp.route("/rotate", methods=["POST"])
def rotate():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        degree = float(request.json["degree"])  # type: ignore
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.rotate(degree)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404


@bp.route("/filp", methods=["POST"])
def filp():
    filename = request.json["filename"]  # type: ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = None
        if request.json["direction"] == "horizontal":  # type: ignore
            out = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            out = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for("download_file", name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404
