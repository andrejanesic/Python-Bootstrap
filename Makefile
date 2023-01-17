init:
    python -m venv env
    ./env/Scripts/activate
	pip install -r requirements.txt

dev:
    ./env/Scripts/activate
	rm -rf sandbox
	mkdir sandbox
	cp start.py sandbox
	cd sandbox
	cd ..
    python start.py

test:
    ./env/Scripts/activate
    python -m tests

build:
    ./env/Scripts/activate
    python setup.py sdist