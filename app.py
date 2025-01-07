from flask import Flask, jsonify, send_file
from flask_cors import CORS
from data.projects import projects_data

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow cross-domain requests


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/projects", methods=["GET"])
def projects():
    return jsonify({"projects": projects_data})


@app.route("/api/projects/<id>", methods=["GET"])
def get_project_by_id(id):
    project = None
    for p in projects_data:
        if p["id"] == id:
            project = p

    if project:
        return jsonify(project)
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route("/api/resume", methods=["GET"])
def resume_file():
    try:
        # pdf path
        file_path = "./data/Xuancheng_Zhou_Resume.pdf"

        # use send_file to send pdf
        return send_file(file_path, as_attachment=True)

    except FileNotFoundError:
        # if not found, return 404
        return jsonify({"error": "Resume file not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
