VERSION=0.2.0

fmt:
	black src/homed.py

build:
	@echo "Building image" && \
	docker build --no-cache=true --rm -t mwalters/homed:$(VERSION) -t mwalters/homed:latest  .

run:
	docker run --rm -d --name homed -e ENV=development -p 5050:5000 -v /Users/mwalters/tmp/test:/config mwalters/homed:$(VERSION) && \
	docker logs -f homed

stop:
	docker stop mwalters/homed

push-prerelease:
	docker buildx build --push --platform linux/arm/v7,linux/arm64/v8,linux/amd64 -t mwalters/homed:$(VERSION) .

push:
	docker buildx build --push --platform linux/arm/v7,linux/arm64/v8,linux/amd64 -t mwalters/homed:latest -t mwalters/homed:$(VERSION) .
