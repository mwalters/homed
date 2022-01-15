from flask import Flask, render_template, send_from_directory, request
from logging.config import dictConfig
from operator import itemgetter
import os, sys, yaml, logging, feedparser

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route("/")
def display_home():
    config = read_config()
    user = get_user(request.headers)
    sections = auth_links(
        sorted(config["sections"], key=itemgetter("order")), request.headers
    )

    weather = get_weather(sections)

    app.logger.info("user={user}, path=/".format(user=user["username"]))

    ui_mode = (
        "dark-mode" if "dark_mode" in config and config["dark_mode"] else "light-mode"
    )

    return render_template(
        "./home.html",
        config=config,
        ui_mode=ui_mode,
        user=user,
        weather=weather,
        sections=sections,
    )


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("assets/css", path)


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("assets/js", path)


# Custom user CSS
@app.route("/custom/css/<path:path>")
def send_custom_css(path):
    return send_from_directory("/config/app/assets/css/", path)


# Custom user JS
@app.route("/custom/js/<path:path>")
def send_custom_js(path):
    return send_from_directory("/config/app/assets/js/", path)


@app.route("/sprites/<path:path>")
def send_sprites(path):
    return send_from_directory("assets/sprites", path)


@app.route("/svgs/<path:path>")
def send_svgs(path):
    return send_from_directory("assets/svgs", path)


@app.route("/webfonts/<path:path>")
def send_webfonts(path):
    return send_from_directory("assets/webfonts", path)


@app.route("/logos/<path:path>")
def send_logos(path):
    return send_from_directory("assets/logos", path)


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


def read_config():
    parsed_yaml_file = yaml.load(open("/config/app/homed.yaml"), Loader=yaml.FullLoader)
    return parsed_yaml_file


def auth_links(sections, headers):
    if "Remote-Groups" in headers:
        groups = headers["Remote-Groups"].split(",")
        for section in sections:
            if "type" in section:
                continue
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


def get_weather(sections):
    weather = {"radar": False, "alerts": []}
    for section in sections:
        if "type" in section and section["type"] == "weather":
            weather_code = section["weather_code"]
            weather_radar = section["weather_radar"]
            app.logger.warning(weather_radar)

            feed = feedparser.parse(
                "https://alerts.weather.gov/cap/wwaatmget.php?x={weather_code}&y=0".format(
                    weather_code=weather_code
                )
            )
            alerts = []
            for entry in feed.entries:
                alerts.append(
                    {
                        "title": entry.title,
                        "summary": entry.summary,
                        "effective": entry.cap_effective,
                        "link": entry.link,
                    }
                )
                app.logger.info("=== Weather Alerts ===")
                app.logger.info(alerts)

            weather = {
                "system_on": True,
                "forecast": "https://www.weather.gov/{weather_radar}/".format(
                    weather_radar=weather_radar
                ),
                "radar": "https://radar.weather.gov/ridge/lite/K{weather_radar}_loop.gif".format(
                    weather_radar=weather_radar
                ),
                "alerts": alerts,
            }
    return weather
