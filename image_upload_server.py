import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400

    if file:
        npimg = np.fromfile(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return (
                jsonify({"success": False, "message": "Could not read image"}),
                400,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Image uploaded and read successfully",
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
