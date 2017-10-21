RUN_PYTHON = docker-compose run --rm --entrypoint pipenv app run python

install:
	docker-compose run --rm --entrypoint pipenv app install

test:
	docker-compose run --rm --entrypoint pipenv app run python -m pytest --pyargs scraper

run:
	${RUN_PYTHON} main.py $(URL)
