from flask import Flask, render_template, send_from_directory, request
from logging.config import dictConfig
from operator import itemgetter
import os, sys, re, yaml, logging, feedparser, requests, datetime

version = "1.2.1"

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

app.logger.info("==== Environment: " + os.environ["FLASK_ENV"])


@app.route("/")
def display_home():
    config = enrich_config()
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
        version=version,
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
    return send_from_directory("/config/app/assets/logos", path)


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


def enrich_config():
    config_file = (
        "/config/app/homed.yaml"
        if os.environ["FLASK_ENV"] == "production"
        else "homed.yaml"
    )
    config = yaml.load(open(config_file), Loader=yaml.FullLoader)

    if "motd" not in config:
        config["motd"] = {"enabled": False}
    if "enabled" not in config["motd"]:
        config["motd"]["enabled"] = True

    for section in config["sections"]:
        if "name" in section:
            if "css_classes" not in section:
                section["css_classes"] = []
            section["css_classes"].append(
                "section-" + re.sub("[^0-9a-zA-Z]+", "-", section["name"].lower())
            )

        if "type" not in section:
            section["type"] = "links"

        if section["type"] == "links":
            for link in section["links"]:
                if "context" not in link:
                    link["context"] = ""

                if "css_classes" not in link:
                    link["css_classes"] = []

                if link["context"] != "":
                    link["css_classes"].append("list-group-item-" + link["context"])

    return config


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
            weather_radar = section["weather_radar"]

            r = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}&units=imperial".format(
                    zip_code=section["zipcode"], api_key=section["openweather_api_key"]
                )
            )
            current_conditions = r.json()

            if "wind" in current_conditions:
                current_conditions["wind"]["wind_deg_human"] = wind_deg_to_dir(
                    current_conditions["wind"]["deg"]
                )
                current_conditions["sys"][
                    "sunrise_human"
                ] = datetime.datetime.fromtimestamp(current_conditions["sys"]["sunrise"])
                current_conditions["sys"]["sunset_human"] = datetime.datetime.fromtimestamp(
                    current_conditions["sys"]["sunset"]
                )
                current_conditions["sys"]["sunrise_human"] = current_conditions["sys"][
                    "sunrise_human"
                ].strftime("%I:%M %p")
                current_conditions["sys"]["sunset_human"] = current_conditions["sys"][
                    "sunset_human"
                ].strftime("%I:%M %p")

                r = requests.get(
                    "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely&appid={api_key}&units=imperial".format(
                        lat=current_conditions["coord"]["lat"],
                        lon=current_conditions["coord"]["lon"],
                        api_key=section["openweather_api_key"],
                    )
                )
                forecast = r.json()

                hourly = []
                for hour in forecast["hourly"]:
                    hour["dt"] = datetime.datetime.fromtimestamp(hour["dt"])
                    hour["dt_human"] = hour["dt"].strftime("%I:%M %p")
                    if hour["dt"].strftime("%H") in [
                        "00",
                        "03",
                        "06",
                        "09",
                        "12",
                        "15",
                        "18",
                        "21",
                    ]:
                        hourly.append(hour)

                    hour["wind_deg_human"] = wind_deg_to_dir(round(hour["wind_deg"]))

                del hourly[5:]
                forecast["hourly"] = hourly

                for day in forecast["daily"]:
                    day["wind_deg_human"] = wind_deg_to_dir(round(day["wind_deg"]))
                    day["dt"] = datetime.datetime.fromtimestamp(day["dt"])
                    day["dt_human"] = day["dt"].strftime("%A")
                    day["sunrise"] = datetime.datetime.fromtimestamp(day["sunrise"])
                    day["sunrise_human"] = day["sunrise"].strftime("%I:%M %p")
                    day["sunset"] = datetime.datetime.fromtimestamp(day["sunset"])
                    day["sunset_human"] = day["sunset"].strftime("%I:%M %p")

                del forecast["daily"][5:]

                alerts = []
                if "alerts" in forecast:
                    for alert in forecast["alerts"]:
                        alert["start"] = datetime.datetime.fromtimestamp(alert["start"])
                        alert["start_human"] = alert["start"].strftime("%Y-%m-%d %I:%M")
                        alert["end"] = datetime.datetime.fromtimestamp(alert["end"])
                        alert["end_human"] = alert["end"].strftime("%Y-%m-%d %I:%M")
                        alert["timerange_human"] = "{start} - {end}".format(
                            start=alert["start"].strftime("%b %d %I:%M %p"),
                            end=alert["end"].strftime("%b %d %I:%M %p"),
                        )

                        alert["description"] = alert["description"].replace("\n", " ")
                        alert["description"] = alert["description"].replace(
                            "* WHAT", "<br><br>* WHAT"
                        )
                        alert["description"] = alert["description"].replace(
                            "* WHERE", "<br><br>* WHERE"
                        )
                        alert["description"] = alert["description"].replace(
                            "* WHEN", "<br><br>* WHEN"
                        )
                        alert["description"] = alert["description"].replace(
                            "* IMPACTS", "<br><br>* IMPACTS"
                        )

                        alerts.append(alert)

                weather = {
                    "system_on": True,
                    "nws_forecast": "https://www.weather.gov/{weather_radar}/".format(
                        weather_radar=weather_radar
                    ),
                    "radar": "https://radar.weather.gov/ridge/lite/K{weather_radar}_loop.gif".format(
                        weather_radar=weather_radar
                    ),
                    "current_conditions": current_conditions,
                    "forecast": forecast,
                    "weather_radar": weather_radar,
                    "alerts": alerts,
                }
            else:
                weather = {
                    "system_on": False
                }
    return weather


def wind_deg_to_dir(wind_deg):
    wind_deg_human = "?"
    if wind_deg >= 348.75 or wind_deg <= 11.25:
        wind_deg_human = "N"
    if wind_deg >= 11.25 and wind_deg <= 33.75:
        wind_deg_human = "NNE"
    if wind_deg >= 33.75 and wind_deg <= 56.25:
        wind_deg_human = "NE"
    if wind_deg >= 56.25 and wind_deg <= 78.75:
        wind_deg_human = "ENE"
    if wind_deg >= 78.75 and wind_deg <= 101.25:
        wind_deg_human = "E"
    if wind_deg >= 101.25 and wind_deg <= 123.75:
        wind_deg_human = "ESE"
    if wind_deg >= 123.75 and wind_deg <= 146.25:
        wind_deg_human = "SE"
    if wind_deg >= 146.25 and wind_deg <= 168.75:
        wind_deg_human = "SSE"
    if wind_deg >= 168.75 and wind_deg <= 191.25:
        wind_deg_human = "S"
    if wind_deg >= 191.25 and wind_deg <= 213.75:
        wind_deg_human = "SSW"
    if wind_deg >= 213.75 and wind_deg <= 236.25:
        wind_deg_human = "SW"
    if wind_deg >= 236.25 and wind_deg <= 258.75:
        wind_deg_human = "WSW"
    if wind_deg >= 258.75 and wind_deg <= 281.25:
        wind_deg_human = "W"
    if wind_deg >= 281.25 and wind_deg <= 303.75:
        wind_deg_human = "WNW"
    if wind_deg >= 303.75 and wind_deg <= 326.25:
        wind_deg_human = "NW"
    if wind_deg >= 326.25 and wind_deg <= 348.75:
        wind_deg_human = "NNW"
    if wind_deg_human == "?":
        wind_deg_human = string(round(wind_deg)) + "deg"
    return wind_deg_human
