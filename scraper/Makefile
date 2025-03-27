URL = "https://thehackernews.com/search/label/Cyber%20Attack"

all: final.json

final.json: scrape.json
	./cleaner.py scrape.json final.json

scrape.json:
	./scraper.py $(URL) scrape.json

clean:
	rm -f scrape.json final.json

VENV_DIR = PRI

activate: 
	source $(VENV_DIR)/bin/activate

final_python: final.json
	python -m scraper $(URL) novo.json
	python -m cleaner novo.json final.json

python_clean: 
	sh -c "source $(VENV_DIR)/bin/activate; rm -f scrape.json final.json"
