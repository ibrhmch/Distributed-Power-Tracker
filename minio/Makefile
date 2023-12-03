VERSION=v4
DOCKERUSER=rylanm14

build:
	docker build -t minio-storage .

push:
	docker tag minio-storage $(DOCKERUSER)/minio-storage:$(VERSION)
	docker push $(DOCKERUSER)/minio-storage:$(VERSION)
	docker tag minio-storage $(DOCKERUSER)/minio-storage:latest
	docker push $(DOCKERUSER)/minio-storage:latest