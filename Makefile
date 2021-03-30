.PHONY: build
build: env
	docker-compose build

.PHONY: run
run:
	docker-compose run vaccine_checker

.PHONY: env
env:
	cp .env.example .env