from flask import (
    Flask,
    jsonify,
    send_file,
    request,
    url_for,
    send_from_directory,
    abort,
)
from flask_cors import CORS
from data.projects import projects_data
from data.birthday_data import birthday_data
import os

# 配置静态文件存放路径（使用绝对路径）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "data/musics")
IMAGE_DIR = os.path.join(BASE_DIR, "data/images")

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})


# get all the projects
@app.route("/api/projects", methods=["GET"])
def projects():
    return jsonify({"projects": projects_data})


# get one specific project
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


# get pdf resume
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


# 获取人物生日相关信息
@app.route("/api/birthday", methods=["POST"])  # 使用 POST
def get_birthday_music():
    data = request.json  # 获取 POST 请求的 JSON 数据
    friend_name = data.get("friend_name")  # 解析 friend_name 参数

    if not friend_name:
        return jsonify({"error": "Missing friend_name"}), 400

    if friend_name in birthday_data:
        person_info = birthday_data[friend_name]
        music_filename = person_info["music_path"]
        cake_filename = person_info["cake_path"]
        carousel_filename = person_info["carousel_path"]
        date = person_info["date"]
        name = person_info["name"]
        message = person_info["message"]

        return jsonify(
            {
                "date": date,
                "name": name,
                "message": message,
                "music": url_for(
                    "serve_music", filename=music_filename, _external=True
                ),
                "cake": url_for("serve_image", filename=cake_filename, _external=True),
                "carousel": url_for(
                    "serve_image", filename=carousel_filename, _external=True
                ),
            }
        )
    else:
        return jsonify({"error": f"No birthday data found for {friend_name}"}), 404


# 获取音乐route
@app.route("/api/music/<path:filename>")
def serve_music(filename):
    file_path = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_from_directory(MUSIC_DIR, filename)


# 获取图片route
@app.route("/api/images/<path:filename>")
def serve_image(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_from_directory(IMAGE_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
