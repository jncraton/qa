all: test

test:
	python3 -m doctest qa.py

clean:
	rm -rf __pycache__
