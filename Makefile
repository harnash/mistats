VERSION := 0.0.1
BUILD_TIME := `date +%FT%T%z`

SERVICE_NAME := purifier2prometheus
DOCKER_IMAGE := service.harnash.com:5000/services/$(SERVICE_NAME)
DOCKER_PORT := 80
SHELL := /bin/sh

docker_build:
	docker build -t ${DOCKER_IMAGE}:${VERSION} ./

docker_run:
	docker run --net=host -t ${DOCKER_IMAGE}:${VERSION}

docker_run_shell:
	docker run --net=host --entrypoint=${SHELL} -ti ${DOCKER_IMAGE}:${VERSION}

docker_upload_image:
	docker push ${DOCKER_IMAGE}:${VERSION}

.PHONY: docker_build
