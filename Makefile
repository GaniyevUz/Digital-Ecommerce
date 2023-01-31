mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	./manage.py createsuperuser --username admin --email admin@example.com

data:
	./manage.py loaddata currency.json
	./manage.py loaddata category.json


unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete