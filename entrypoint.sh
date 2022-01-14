#!/usr/bin/env sh

echo "Copying files"
cp -r --no-clobber /app /config

cd /config/app

pwd

export FLASK_APP=homed
export FLASK_ENV=${ENV:-production}
python3 -m flask run --host=0.0.0.0 -p 5000
