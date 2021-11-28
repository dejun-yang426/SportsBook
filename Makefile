# The Python executable to use.
PYTHON = python3.9

TEST_DIR = test
TESTS_PY_FILES = $(shell find $(TEST_DIR) -type f -name 'test_*.py')

all: setup test run clean

setup: requirements.txt
   @pip install -r requirements.txt

# Run all of the unit tests and show the coverage results.
test: $(TESTS_PY_FILES)
	@$(PYTHON) -m unittest -v $^

run:
    @./venv/Scripts/active
    @export FLASK_ENV=development
    @export FLASK_APP=app.py
    @flask run

clean:
	@find . \( -name '*.pyc' \) -exec rm {} \;
