.PHONY: install check test docs-serve docs-deploy

install:
	pip install -e ".[dev,docs]"
	pre-commit install

check:
	black .
	isort .
	ruff check . --fix

test:
	PYTHONPATH=. pytest tests/ projects/

docs-serve:
	fuser -k 8009/tcp || true
	mkdocs serve -a 127.0.0.1:8009

docs-deploy:
	mkdocs gh-deploy --clean

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type f -name ".secrets.baseline" -delete
