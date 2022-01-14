#!/usr/bin/env bash

. venv/bin/activate

cd src

export FLASK_APP=homed
export FLASK_ENV=development

flask run

# clean:
#     docker ps -a | awk '{ print $1,$2 }' | grep mwalters/homed | awk '{print $1 }' | xargs -I {} docker rm {}

# clean-images:
#     docker rmi $(docker images 'mwalters/homed' -a -q)

