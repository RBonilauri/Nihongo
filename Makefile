.PHONY: build test release
build:
	python3 src/build.py
test: build
	python3 tests/test_app.py
release: test
	python3 src/release.py
