from flask import Flask, jsonify, request, send_from_directory
from actions import bp as actionsbp
from android import bp as androidbp
from filters import bp as filtersbp
from helpers import *
import boto3, botocore
from dotenv import load_dotenv
from flask_restx import Api, Resource, fields

# get value from .env
load_dotenv()

# determin the folder for upload image to it
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSION = ["png", "jpg", "jpeg"]
DOWNLOAD_FOLDER = "downloads/"

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Image Processing API",
    description="API for uploading and resizing images",
)
app.secret_key = os.getenv("app_secret_key")

app.config["S3_BUCKET"] = os.getenv("bucket")
app.config["S3_KEY"] = os.getenv("key")
app.config["S3_SECRET"] = os.getenv("secret_key")
app.config["S3_LOCATION"] = os.getenv("server_location")

# add folder to app configeration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSION"] = ALLOWED_EXTENSION
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

app.register_blueprint(actionsbp)
app.register_blueprint(androidbp)
app.register_blueprint(filtersbp)


@app.route("/")
def welcome():
    return jsonify({"message": "Welcome to our images api "})


@app.route("/images", methods=["POST", "GET"])  # type: ignore
def images():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file was selected"}), 400
        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file was selected"}), 400

        if not allowed_extension(file.filename):
            return jsonify({"error": "There extension is not support "})

        #
        output = upload_to_s3(file, app.config["S3_BUCKET"])
        # file.save(filepath)
        return (
            jsonify({"message": "file successfully uploadedd", "filename": output}),
            201,
        )
    images = []
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=app.config["S3_KEY"],
        aws_secret_access_key=app.config["S3_SECRET"],
    )
    s3_bucket = s3_resource.Bucket(app.config["S3_BUCKET"])
    for obj in s3_bucket.objects.filter(Prefix="uploads/"):
        if obj.key == "uploads/":
            continue
        images.append(obj.key)
    return jsonify({"data": images}), 200


@app.route("/downloads/<name>")
def download_file(name):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)
