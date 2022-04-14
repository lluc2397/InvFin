.PHONY: requirements

build:
	docker-compose -f local.yml build

up-back:
	docker-compose -f local.yml up -d

up:
	docker-compose -f local.yml up

stop:
	docker-compose -f local.yml stop

shell:
	docker-compose -f local.yml exec invfin_local_django /bin/sh

shell_db:
	docker-compose -f local.yml exec invfin_local_postgres /bin/sh

dbshell:
	docker-compose -f local.yml run --rm invfin_local_django python -u manage.py dbshell

log:
	docker-compose -f local.yml logs -f invfin_local_django

log-db:
	docker-compose -f local.yml logs db

migrations:
	docker-compose -f local.yml run --rm invfin_local_django python -u manage.py makemigrations $(ar)

migrate:
	docker-compose -f local.yml run --rm invfin_local_django python -u manage.py migrate $(ar)

pep:
	docker-compose -f local.yml run --rm invfin_local_django flake8

docs_check:
	docker-compose -f local.yml run --rm invfin_local_django ./manage.py generate_swagger --settings=config.settings.local

test:
	docker-compose -f local.yml run --rm invfin_local_django python -u manage.py test $(ar) --noinput --settings=config.settings.test

cov:
	docker-compose -f local.yml run --rm invfin_local_django coverage run --source='.' manage.py test $(ar) --noinput --settings=config.settings.test
	docker-compose -f local.yml run --rm invfin_local_django coverage report

shell_plus:
	docker-compose -f local.yml run --rm invfin_local_django ./manage.py shell_plus

manage:
	docker-compose -f local.yml run --rm invfin_local_django ./manage.py $(ar) --settings=config.settings.local

run:
	docker-compose -f local.yml run --rm invfin_local_django $(ar)

pdb:
	docker-compose -f local.yml stop invfin_local_django
	docker-compose -f local.yml run --rm --service-ports invfin_local_django

pdb_manage:
	docker-compose -f local.yml stop invfin_local_django
	docker-compose -f local.yml run --rm --service-ports invfin_local_django  ./manage.py $(ar) --settings=config.settings.local

isort:
	docker-compose -f local.yml run --rm invfin_local_django isort -rc -y

isort_pep:
	docker-compose -f local.yml run --rm invfin_local_django bash -c "isort -rc -y && flake8"

isort_check:
	docker-compose -f local.yml run --rm invfin_local_django isort -rc -c
