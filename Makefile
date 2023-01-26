mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	./manage.py createsuperuser --username admin --email admin@example.com

cl_data:
	./manage.py collect_data

clear_mig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete