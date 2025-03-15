from flask import Flask, request, jsonify
import os
import threading
import uuid
from printer import print_file
from db import log_print_job

# Define the uploads folder (ensure this folder exists and is writable)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def background_print(file_path):
    try:
        print_file(file_path)
    except Exception as e:
        print(f"Error during background printing: {e}")

@app.route('/print', methods=['POST'])
def print_document():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected"}), 400

    # Generate a unique filename using uuid and preserve the original extension
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    # Log the print job to the database
    log_print_job(unique_filename, file_path)

    # Start the printing process in a background thread
    threading.Thread(target=background_print, args=(file_path,)).start()

    return jsonify({"status": "success", "message": "Printing started"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
