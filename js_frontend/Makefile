VERSION=v1
DOCKERUSER=rylanm14

build:
	docker build -f Dockerfile -t proj-map-server .

push:
	# docker tag proj-map-server $(DOCKERUSER)/proj-map-server:$(VERSION)
	# docker push $(DOCKERUSER)/proj-map-server:$(VERSION)
	docker tag proj-map-server $(DOCKERUSER)/proj-map-server:latest
	docker push $(DOCKERUSER)/proj-map-server:latest
