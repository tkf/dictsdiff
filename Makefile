PROJECT = dictsdiff

.PHONY: test clean clean-pycache inject-readme upload

## Testing
test: inject-readme
	tox

test-cov: test-cov-py27 test-cov-py36

test-cov-py27 test-cov-py36: \
test-cov-%: inject-readme
	tox -e $* -- --cov $(PROJECT) --cov-report term \
		--cov-report html:$(PWD)/.tox/$*/tmp/cov_html

clean: clean-pycache
	rm -rf src/*.egg-info .tox MANIFEST

clean-pycache:
	find src -name __pycache__ -o -name '*.pyc' -print0 \
		| xargs --null rm -rf

## Update files using misc/inject_readme.py
inject-readme: src/$(PROJECT)/__init__.py
src/$(PROJECT)/__init__.py: misc/inject_readme.py README.rst
	$<

## Upload to PyPI
upload: inject-readme
	rm -rf dist/
	python setup.py sdist
	twine upload dist/*
