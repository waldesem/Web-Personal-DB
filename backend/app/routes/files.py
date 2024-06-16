import json
import os

from flask import abort, request, send_file
from PIL import Image

from ..tools.depends import jwt_required, user_required
from ..tools.folders import Folders
from ..tools.parsers import Anketa
from ..tools.queries import select_single
from . import bp


@bp.route("/image/<int:item_id>")
@jwt_required()
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.

    Args:
        item_id (int): The ID of the item for which to retrieve the image.

    Returns:
        A response containing the image file if it exists, or a default image file if it does not.
    """
    # Retrieve the person information from the database
    person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))

    # Create a Folders object with the person's information
    folders = Folders(
        person["id"],
        person["surname"],
        person["firstname"],
        person.get("patronymic", ""),
    )

    # Construct the file path to the image file
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")

    # Check if the image file exists
    if os.path.isfile(file_path):
        # If it does, send the file as a response
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    else:
        # If it does not, send the default image file as a response
        return send_file(
            "static/no-photo.png", as_attachment=True, mimetype="image/jpg"
        )

@bp.route("/file/<action>/<int:item_id>", methods=["POST"])
@user_required()
def post(action, item_id=None):
    """
    Handles POST requests to upload files.

    Args:
        action (str): The action to perform. Can be "anketa" or any other folder name.
        item_id (int, optional): The ID of the item if action is "anketa".

    Returns:
        A response with a status code of 201 if the file was uploaded successfully,
        or a response with a status code of 400 if the file was not uploaded successfully.
    """
    # Get the uploaded file from the request
    file = request.files["file"]

    # Check if the file has a filename
    if not file.filename:
        return abort(400)

    # Handle the "anketa" action
    if action == "anketa":
        # Load the JSON data from the file
        json_dict = json.load(file)

        # Create an Anketa object
        anketa = Anketa(json_dict)

        # Parse the anketa and get the person ID
        person_id = anketa.parse_anketa()

        # If the person ID is not None, return a response with a status code of 201
        if person_id:
            return "", 201
        # Otherwise, return a response with a status code of 400
        return abort(400)

    # Handle other actions
    # Get the person information from the database
    person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))

    # Create a Folders object with the person's information
    folders = Folders(
        person["id"],
        person["surname"],
        person["firstname"],
        person.get("patronymic", ""),
    )

    # Handle the "image" action
    if action == "image":
        # Create the parent folder for the image
        folder = folders.create_parent_folder("image")

        # Open the image file
        im = Image.open(file)

        # Convert the image to RGB format
        rgb_im = im.convert("RGB")

        # Construct the file path to the image file
        image_path = os.path.join(folder, "image.jpg")

        # Check if the image file already exists
        if os.path.isfile(image_path):
            # If it does, remove the existing image file
            os.remove(image_path)

        # Save the image file
        rgb_im.save(image_path)

        # Return a response with a status code of 201
        return "", 201

    # Handle other actions
    # Create the subfolder for the action
    folder = folders.create_subfolder(action)

    # Get the list of files uploaded
    files = request.files.getlist("file")

    # Iterate over the uploaded files
    for file in files:
        # Check if the file has a filename
        if file.filename:
            # Construct the file path to the uploaded file
            file_path = os.path.join(folder, file.filename)

            # Check if the file already exists
            if not os.path.isfile(file_path):
                # If it does not, save the file
                file.save(file_path)

    # Return a response with a status code of 201
    return "", 201
