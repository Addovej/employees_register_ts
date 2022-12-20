.DEFAULT_GOAL := help
COMPOSE_RUN_APP := docker-compose run --rm app
pyproject = ../pyproject.toml

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## Build application
	docker-compose build

start:  ## Start application
	docker-compose up -d

generate_migrations:  ## Generate new migrations. Using: make generate_migrations NAME='migration_name'
	$(COMPOSE_RUN_APP) alembic revision --autogenerate -m '$(NAME)'

migrate:  ## Apply migrations
	$(COMPOSE_RUN_APP) alembic upgrade head

downgrade_migration:  ## Downgrade latest migration
	$(COMPOSE_RUN_APP) alembic downgrade -1

lock_poetry:  ## Update poetry.lock file
	$(COMPOSE_RUN_APP) poetry lock

isort:  ## Apply isort tool to the project
	$(COMPOSE_RUN_APP) isort .

flake8:  ## Run flake8
	$(COMPOSE_RUN_APP) flake8

mypy:  ## Run mypy
	$(COMPOSE_RUN_APP) mypy .

tests:  ## Run tests
	$(COMPOSE_RUN_APP) /bin/bash -c "cd /app && pytest -c $(pyproject)"
