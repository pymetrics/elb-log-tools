dist:
	python setup.py sdist

clean:
	rm -rf dist
	find . -name "*.pyc" -delete

test:
	tox --parallel auto

is-newest-version:
	python is_newest_version.py

typecheck:
	mypy elb_log_tools --ignore-missing-imports

publish: is-newest-version clean dist
	twine upload dist/*
