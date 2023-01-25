mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	./manage.py createsuperuser --username admin --email admin@example.com