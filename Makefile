# AWS
AWS_ACCESS_KEY_ID?=AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY?=AWS_SECRET_ACCESS_KEY
AWS_REGION?=AWS_REGION

# run 'make get-deps-dev' prior to running any other targets

# run as a module
run-module: format lint test	
	python -m pyretriever --symbol ^GSPC ^GDAXI --start-date 2019-12-01 --end-date 2019-12-02 --provider=yahoo

# run as a script
run-script:	
	python runner.py

debug-test:
	python -m pytest -s
	
test:	
	coverage run --source pyretriever --omit test_*.py -m pytest
	coverage report -m 
	coverage html

format:
	black pyretriever

lint:	
	flake8 pyretriever
	mypy pyretriever

tox:
	tox

clean-all: clean-docs clean-pyc
	rm -r __pycache__/ || true
	rm -r .mypy_cache/ || true
	rm -r .pytest_cache/ || true
	rm -r .tox/ || true
	rm -r pyretriever.egg* || true
	rm -r htmlcov/ || true
	rm *.log
	
clean-pyc: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	rm -f docs/pyretriever.rst || true
	rm -f docs/modules.rst || true
	rm -fr docs/_build || true

docs-html: clean-docs
	sphinx-apidoc -o docs/ pyretriever
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

bumpversion-patch:
	bump2version patch

bumpversion-minor:
	bump2version minor

bumpversion-major:
	bump2version major

get-deps-dev:
	pipenv install --dev
	pipenv shell

lock-deps:
	pipenv lock

get-deps-prd:
	pipenv install --ignore-pipfile