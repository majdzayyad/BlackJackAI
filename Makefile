.PHONY: all, blackjack, clean  #tells make that all and clean aren’t real targets

#default PARAMS
PARAMS=mdp 1000

all: blackjack

blackjack: venv/bin/activate
	./venv/bin/python3 main.py ${PARAMS}

venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
