# Meta info
NAME := medusa_brain
VERSION := $(shell git describe --tags --abbrev=0)
REVISION := $(shell git rev-parse --short HEAD)
LDFLAGS := -X 'main.version=$(VERSION)' \
		-X 'main.revision=$(REVISON)'

opencv:
	wget -N -P ./res/opencv/ https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml

deps:
	pip install -r requirements.txt

run: deps
	python -m src.medusa

.PHONY: deps run
