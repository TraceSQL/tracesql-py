.PHONY : docs
docs :
	rm -rf docs/build/
	sphinx-autobuild -b html --watch tracesql/ docs/source/ docs/build/

.PHONY : run-checks
run-checks :
	isort --check .
	black --exclude=venv --check .
	ruff check .
	mypy .
	CUDA_VISIBLE_DEVICES='' pytest -v --color=yes --doctest-modules tests/ tracesql/

.PHONY : build
build :
	rm -rf *.egg-info/
	python -m build
