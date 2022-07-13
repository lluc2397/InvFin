BLACK_FOLDERS=apps

.PHONY: requirements

build:
	docker-compose -f local.yml build $(ar)

clean-build:
	docker-compose -f local.yml build --no-cache $(ar)

reboot:
	$(MAKE) stop && $(MAKE) up-b

restart:
	docker-compose -f local.yml restart $(ar)

up-b:
	docker-compose -f local.yml up -d django
	docker-compose -f local.yml logs -f django

up:
	docker-compose -f local.yml up $(ar)

buildsemi:
	docker-compose -f semiprod.yml build

upsemi:
	docker-compose -f semiprod.yml up nginx django

stop:
	docker-compose -f local.yml stop

shell:
	docker-compose -f local.yml exec $(ar) /bin/bash

# Django
up-d:
	docker-compose -f local.yml up django

dbshell:
	docker-compose -f local.yml run --rm django python -u manage.py dbshell --settings=config.settings.local

log:
	docker-compose -f local.yml logs -f django

migrations:
	docker-compose -f local.yml run --rm django python -u manage.py makemigrations $(ar) --settings=config.settings.local

migrate:
	docker-compose -f local.yml run --rm django python -u manage.py migrate $(ar) --settings=config.settings.local

allmig:
	docker-compose -f local.yml run --rm django python -u manage.py makemigrations $(ar) --settings=config.settings.local
	docker-compose -f local.yml run --rm django python -u manage.py migrate $(ar) --settings=config.settings.local

shell_plus:
	docker-compose -f local.yml run --rm django ./manage.py shell_plus --settings=config.settings.local

manage:
	docker-compose -f local.yml run --rm django ./manage.py $(ar) --settings=config.settings.local

collectstatic:
	docker-compose -f local.yml run --rm django ./manage.py collectstatic --noinput --settings=config.settings.local

col-share-static:
	docker-compose -f local.yml run --rm django ./manage.py collectstatic --noinput --settings=config.settings.local
	docker-compose -f local.yml build

run:
	docker-compose -f local.yml run --rm django $(ar)

pip:
	docker exec -ti invfin_local_django pip install $(ar)

pdb:
	docker-compose -f local.yml stop django
	docker-compose -f local.yml run --rm --service-ports django

pdb_manage:
	docker-compose -f local.yml stop django
	docker-compose -f local.yml run --rm --service-ports django  ./manage.py $(ar) --settings=config.settings.local

requirements:
	docker-compose -f local.yml run django /requirements.sh "temp_venv/bin/pip"
	docker-compose -f local.yml run django rm -rf temp_venv/

# Postgres
shell_db:
	docker-compose -f local.yml exec postgres /bin/sh

log-db:
	docker-compose -f local.yml logs db

backup:
	docker-compose -f local.yml exec postgres backup

ls_backups:
	docker-compose -f local.yml exec postgres backups

rt_backups:
	docker cp docker-compose -f local.yml ps -q postgres:/backups ./backups

restore:
	docker-compose -f local.yml exec postgres restore $(ar)

# Documentation
docs_check:
	docker-compose -f local.yml run --rm django ./manage.py generate_swagger --settings=config.settings.local

# Testing
new-test:
	docker-compose -f local.yml run --rm django python -u manage.py test $(ar) --noinput --settings=config.settings.test

test:
	docker-compose -f local.yml run --rm django python -u manage.py test $(ar) --noinput --keepdb --settings=config.settings.local

pytest:
	docker-compose -f local.yml run --rm django pytest

cov:
	docker-compose -f local.yml run --rm django coverage run --source='.' manage.py test $(ar) --noinput --settings=config.settings.test
	docker-compose -f local.yml run --rm django coverage report

pycov:
	docker-compose -f local.yml run --rm django coverage run -m pytest
	docker-compose -f local.yml run --rm django coverage report

# Style
flake:
	docker-compose -f local.yml run django flake8 $(ar)

isort:
	docker-compose -f local.yml run django isort .

black:
	docker-compose -f local.yml run django black ${BLACK_FOLDERS}

format:
	docker-compose -f local.yml run django flake8 && isort . && black ${BLACK_FOLDERS}
