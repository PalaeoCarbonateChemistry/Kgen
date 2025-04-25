.PHONY: test-python, build-python, upload-python, distribute-python, test-crosscheck, pymyami-update

test-python:
	cd python; python -m unittest

test-crosscheck:
	cd crosscheck; python gen_python.py; Rscript gen_r.r; python -m unittest crosscheck.py; rm generated_Ks/*.csv

pymyami-update:
	python update_pymyami.py

build-python:
	cd python; 	python -m build

upload-python:
	cd python; 	twine upload dist/*

distribute-python:
	make test-python
	make build-python
	make upload-python
