.PHONY: default build check-build up down up-deps up-app

include .env
export

default: up

build:
	@docker-compose -f docker-compose.dev.yml build
	@touch .build.timestamp

check-build:
	@if [ -n "$$(find ./app -newer .build.timestamp 2>/dev/null)" ] || \
	   [ ! -f .build.timestamp ] || \
	   [ Dockerfile -nt .build.timestamp ]; then \
		$(MAKE) build; \
	fi

up: check-build
	@docker-compose -f docker-compose.dev.yml up

down:
	@docker-compose -f docker-compose.dev.yml down
	@rm -f .build.timestamp

up-deps:
	@docker-compose -f docker-compose.dev.yml up -d postgres redis

up-app:
	@docker-compose -f docker-compose.dev.yml up app
