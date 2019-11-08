dist:
	python setup.py sdist

clean:
	rm -rf dist
	find . -name "*.pyc" -delete

test:
	tox --parallel auto

is-newest-version:
	python is_newest_version.py

publish: is-newest-version clean dist
	twine upload dist/*
