from flask import Flask, render_template, send_from_directory, request
from logging.config import dictConfig
from operator import itemgetter
import os, sys, yaml, logging

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route("/")
def display_home():
    config = read_config()
    user = get_user(request.headers)
    sections = auth_links(
        sorted(config["sections"], key=itemgetter("order")), request.headers
    )

    app.logger.info("user={user}, path=/".format(user=user["username"]))

    return render_template(
        "./home.html",
        name=config["name"],
        open_links_in_new_window=config["open_links_in_new_window"],
        auth_ui_link=config["auth_ui_link"],
        user=user,
        headers=request.headers,
        sections=sections,
    )


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("assets/css", path)


@app.route("/sprites/<path:path>")
def send_sprites(path):
    return send_from_directory("assets/sprites", path)


@app.route("/svgs/<path:path>")
def send_svgs(path):
    return send_from_directory("assets/svgs", path)


@app.route("/webfonts/<path:path>")
def send_webfonts(path):
    return send_from_directory("assets/webfonts", path)


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("assets/js", path)


@app.route("/logos/<path:path>")
def send_logos(path):
    return send_from_directory("assets/logos", path)


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


def read_config():
    parsed_yaml_file = yaml.load(open("homed.yaml"), Loader=yaml.FullLoader)
    return parsed_yaml_file


def auth_links(sections, headers):
    if "Remote-Groups" in headers:
        groups = headers["Remote-Groups"].split(",")
        for section in sections:
            for idx, link in enumerate(section["links"]):
                if "authGroups" not in link:
                    continue
                for authGroup in link["authGroups"]:
                    if authGroup not in groups:
                        section["links"].pop(idx)

    return sections


def get_user(headers):
    if os.environ["FLASK_ENV"] == "development":
        return {
            "username": "mwalters",
            "name": "Matt",
            "email": "test@testing.com",
            "groups": ["admins", "users"],
        }
    user = {}
    if "Remote-User" in headers:
        user["username"] = headers["Remote-User"]
    if "Remote-Name" in headers:
        user["name"] = headers["Remote-Name"]
    if "Remote-Email" in headers:
        user["email"] = headers["Remote-Email"]
    if "Remote-Groups" in headers:
        user["groups"] = headers["Remote-Groups"].split(",")

    return user
