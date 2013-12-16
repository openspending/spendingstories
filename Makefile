# Makefile -- Spending Stories

WEBAPP     = $(wildcard */webapp.py)

run:
	. `pwd`/.env ; python manage.py runserver

install:
	virtualenv venv --no-site-packages --distribute --prompt=SpendingStories
	. `pwd`/.env ; pip install -r requirements_core.txt
	npm install
	. `pwd`/.env ; python manage.py syncdb && python manage.py migrate

test:
	. `pwd`/.env ; python manage.py test

# EOF
