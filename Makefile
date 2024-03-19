venv/bin/activate: requirements.txt
	@echo "installing requirements..."
	python3 -m venv venv; 
	. venv/bin/activate; 
	venv/bin/pip3 install --upgrade pip;
	venv/bin/pip3 install -r requirements.txt; 
	@echo " ------- install complete -------";

run: test_apis.py venv/bin/activate
	@python3 test_apis.py