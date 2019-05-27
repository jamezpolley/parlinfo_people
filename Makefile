.phony: venv clean

ALL: run

HOSTNAME := $(shell hostname)

venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip virtualenv
	.venv/bin/pip install -Ur requirements.txt

run: venv
	.venv/bin/python3 scraper.py

clean:
	rm -rf .venv