# AWS
AWS_ACCESS_KEY_ID?=AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY?=AWS_SECRET_ACCESS_KEY
AWS_REGION?=AWS_REGION

# run 'make get-deps-dev' prior to running any other targets

# run as a module
run-module: format lint test	
	python -m pyanalysis --symbol ^GSPC ^GDAXI --start-date 2019-12-01 --end-date 2019-12-02 --provider=yahoo --file-name=df.csv --bucket-name=stock --log-level=DEBUG

run-entry-point: uninstall-wheel clean build-wheel install-wheel
	.venv/bin/pyanalysis-retriever --symbol ^GSPC ^GDAXI --start-date 2019-12-01 --end-date 2019-12-02 --provider=yahoo --file-name=df.csv --bucket-name=stock --log-level=DEBUG

# run as a script
run-script:	
	python runner.py

debug-test:
	python -m pytest -s
	# using more processes makes it slower for a small number of tests
	# --numprocesses=auto
	
test:	
	coverage run --source pyanalysis --omit test_*.py -m pytest
	coverage report -m 
	coverage html

format:
	black --line-length=79 pyanalysis

lint:	
	flake8 pyanalysis
	mypy pyanalysis
	pycodestyle pyanalysis

tox:
	tox

clean-all: clean
	rm -r .venv/ || true

clean: clean-docs clean-pyc
	rm -r __pycache__/ || true
	rm -r .mypy_cache/ || true
	rm -r .pytest_cache/ || true
	rm -r .tox/ || true
	rm -r pyanalysis.egg* || true
	rm -r htmlcov/ || true
	rm *.log || true
	rm -r build/ || true
	rm -r dist/ || true
	rm df.csv || true
	
clean-pyc: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	rm -f docs/pyanalysis.rst || true
	rm -f docs/modules.rst || true
	rm -fr docs/_build || true

docs-html: clean-docs
	sphinx-apidoc -o docs/ pyanalysis
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

bumpversion-patch:
	bump2version patch

bumpversion-minor:
	bump2version minor

bumpversion-major:
	bump2version major

deps-dev:
	pipenv install --dev
	pipenv shell

lock-deps:
	pipenv lock

deps-prd:
	pipenv install --ignore-pipfile

build-wheel: clean
	python setup.py bdist_wheel

build-sdist: clean
	python setup.py sdist

install-wheel:
	pip install dist/pyanalysis-version_0.0.1_-py3-none-any.whl

uninstall-wheel:
	pip uninstall -y pyanalysis

run-wheel: # must be done after installing the wheel
	# run directly from the wheel file
	# python dist/pyanalysis-version_0.0.1_-py3-none-any.whl/pyanalysis
	# or use the module
	cd ~ && python -m pyanalysis

distribute:
	#python setup.py register pyanalysis
	#python setup.py sdist upload -r testpypi
	# OR #
	#python setup.py bdist_wheel upload -r testpypi

install-setup:
	python setup.py install 

uninstall-setup:
	rm .venv/lib/python3.8/site-packages/pyanalysis-version_0.0.1_-py3.8.egg || true
	rm .venv/bin/pyanalysis-retriever || true
