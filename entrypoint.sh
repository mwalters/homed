#!/usr/bin/env sh

echo "===================="
echo "Copying files if they do not already exist"
mkdir -p /config/app/assets/css
mkdir -p /config/app/assets/js
mkdir -p /config/app/assets/logos
cp -r --no-clobber /app/homed.yaml /config/app/homed.yaml
cp -r --no-clobber /app/assets/css/custom.css /config/app/assets/css/custom.css
cp -r --no-clobber /app/assets/js/custom.js /config/app/assets/js/custom.js
cp -r --no-clobber /app/assets/logos/* /config/app/assets/logos
ls -Rla /config
echo "===================="

echo "===================="
echo "Starting application"
export FLASK_APP=homed
export FLASK_ENV=${ENV:-production}
python3 -m flask run --host=0.0.0.0 -p 5000
