UNAME=$(shell uname -s)

style:
	flake8 .

types:
	mypy .

test:
#	pytest -q --cov=. --cov-report=xml

check:
	make test style types

install-dev:
ifeq ($(UNAME),Darwin)
	LDFLAGS="-L/usr/local/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/readline/lib" pip-sync requirements.txt
else
	pip-sync requirements.txt
endif

install-hooks:
	pre-commit install -t pre-commit -t commit-msg -t pre-push

migrations:
	cd app && alembic revision --autogenerate -m "$(name)"

migrate:
	cd app && alembic upgrade head
