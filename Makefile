.PHONY: requirements

build:
	docker-compose -f local.yml build

up-back:
	docker-compose -f local.yml up -d

up:
	sensible-browser 0.0.0.0:8000 &
	sensible-browser 0.0.0.0:8000/admin &
	sensible-browser 0.0.0.0:8025 &
	sensible-browser 0.0.0.0:5555 &
	docker-compose -f local.yml up

stop:
	docker-compose -f local.yml stop

# Django
shell:
	docker-compose -f local.yml exec django /bin/sh

dbshell:
	docker-compose -f local.yml run --rm django python -u manage.py dbshell --settings=config.settings.local

log:
	docker-compose -f local.yml logs -f django

migrations:
	docker-compose -f local.yml run --rm django python -u manage.py makemigrations $(ar) --settings=config.settings.local

migrate:
	docker-compose -f local.yml run --rm django python -u manage.py migrate $(ar) --settings=config.settings.local

shell_plus:
	docker-compose -f local.yml run --rm django ./manage.py shell_plus --settings=config.settings.local

manage:
	docker-compose -f local.yml run --rm django ./manage.py $(ar) --settings=config.settings.local

run:
	docker-compose -f local.yml run --rm django $(ar) --settings=config.settings.local

pdb:
	docker-compose -f local.yml stop django
	docker-compose -f local.yml run --rm --service-ports django

pdb_manage:
	docker-compose -f local.yml stop django
	docker-compose -f local.yml run --rm --service-ports django  ./manage.py $(ar) --settings=config.settings.local

# Postgres
shell_db:
	docker-compose -f local.yml exec postgres /bin/sh

log-db:
	docker-compose -f local.yml logs db

backup:
	docker-compose -f local.yml exec postgres backup

ls-backups:
	docker-compose -f local.yml exec postgres backups

cp-backups:
	docker cp $(docker-compose -f local.yml ps -q postgres):/backups ./backups

restore:
	docker-compose -f local.yml exec postgres restore $(ar)

# Documentation
docs_check:
	docker-compose -f local.yml run --rm django ./manage.py generate_swagger --settings=config.settings.local

# Testing
test:
	docker-compose -f local.yml run --rm django python -u manage.py test $(ar) --noinput --settings=config.settings.test

pytest:
	docker-compose -f local.yml run --rm django pytest

cov:
	docker-compose -f local.yml run --rm django coverage run --source='.' manage.py test $(ar) --noinput --settings=config.settings.test
	docker-compose -f local.yml run --rm django coverage report

pycov:
	docker-compose -f local.yml run --rm django coverage run -m pytest
	docker-compose -f local.yml run --rm django coverage report

# Style
pep:
	docker-compose -f local.yml run --rm django flake8

isort:
	docker-compose -f local.yml run --rm django isort -rc -y

isort_pep:
	docker-compose -f local.yml run --rm django bash -c "isort -rc -y && flake8"

isort_check:
	docker-compose -f local.yml run --rm django isort -rc -c
