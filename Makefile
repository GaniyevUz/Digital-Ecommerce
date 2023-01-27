mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	./manage.py createsuperuser --username admin --email admin@example.com

data:
	./manage.py loaddata shop_currency.yaml
	./manage.py loaddata shop_category.yaml


unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete