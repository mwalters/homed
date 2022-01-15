# homed

* [GitHub Repo](https://github.com/mwalters/homed)
* [Docker Hub](https://hub.docker.com/r/mwalters/homed)

`homed` is a light-weight customizable portal primarily intended for the "self-hosted" crowd with built-in support for local authentication services (e.g. [Authelia](https://www.authelia.com/)).  The user configures options and which links to display using a `yaml` file, and also has ability to include custom CSS and JavaScript.  All resources are hosted locally.  Access to links is controlled via groups passed in by the authentication service using the `Remote-Groups` request header (which Authelia supports).

<img src="https://github.com/mwalters/homed/raw/main/screenshots/homed.png?raw=true" alt="homed" width="100%">

Optional Weather section that can be configured:<br>
<img src="https://github.com/mwalters/homed/raw/main/screenshots/homed-weather-section.png?raw=true" alt="homed" width="100%">

## A note on customization
If you do choose to customize the HTML, it could make upgrading in the future difficult in terms of taking advantage of new features that may require updates to the HTML itself.  So weigh how important future features might be to you before choosing to customize the html.

## Features
* Auth integration (e.g. [Authelia](https://www.authelia.com/))
* Full access to HTML, CSS, JavaScript
* Simple `yaml` configuration file
* FontAwesome icon support
* Light/Dark mode

## Documentation
Please visit the [wiki](https://github.com/mwalters/homed/wiki)

## Versioning
Semver will be followed.  For version `x.y.z`

* `x` Major version release, breaking changes
* `y` Minor version release, no breaking changes, added features
* `z` Bug release, no breaking changes, no new features
