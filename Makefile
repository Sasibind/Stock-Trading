commit:
	git add .
	git commit -m $(m)
	git push -u origin main

initdb:
	python initdb.py