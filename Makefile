BUILD_TIME := `date +%FT%T%z`

SERVICE_NAME := mistats
DOCKER_IMAGE := service.harnash.com:5000/services/$(SERVICE_NAME)
DOCKER_PORT := 80
SHELL := /bin/sh

# Injecting project version and build time
ifeq ($(OS),Windows_NT)
	VERSION := $(shell cmd /C 'git describe --always --tags --abbrev=7')
else
	VERSION_GIT := $(shell sh -c 'git describe --always --tags --abbrev=7')
	VERSION = $(shell echo ${VERSION_GIT\#v})
endif

ifeq ($(VERSION),)
	VERSION = 0.3.3
endif

docker_build:
	docker build -t ${DOCKER_IMAGE}:${VERSION} ./

docker_run:
	docker run --net=host -t ${DOCKER_IMAGE}:${VERSION}

docker_run_shell:
	docker run --net=host --entrypoint=${SHELL} -ti ${DOCKER_IMAGE}:${VERSION}

docker_upload: docker_build
	docker push ${DOCKER_IMAGE}:${VERSION}
	docker tag ${DOCKER_IMAGE}:${VERSION} harnash/${SERVICE_NAME}:${VERSION}
	docker push harnash/${SERVICE_NAME}:${VERSION}

.PHONY: docker_build
