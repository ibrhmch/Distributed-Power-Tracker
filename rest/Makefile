VERSION=v2
DOCKERUSER=rylanm14

build:
	docker build -f Dockerfile -t proj-rest-server .

push:
	# docker tag proj-rest-server $(DOCKERUSER)/proj-rest-server:$(VERSION)
	# docker push $(DOCKERUSER)/proj-rest-server:$(VERSION)
	docker tag proj-rest-server $(DOCKERUSER)/proj-rest-server:latest
	docker push $(DOCKERUSER)/proj-rest-server:latest
