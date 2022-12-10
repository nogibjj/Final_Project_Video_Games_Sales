install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	pylint --disable=R,C main.py mylib/*.py
format:
	black *.py mylib/*.py
