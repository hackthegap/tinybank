# Tiny Bank

## Done by Fabricio + Holly + students of the fullstack-s25

### From the backoffice folder, run:
```
docker-compose build
```
```
# optional
docker-compose run backend python manage.pycreatesuperuser 
```
```
docker-compose run backend python manage.py makemigrations core
```
```
docker-compose run backend python manage.py migrate 
```
## Running the backend + client + backoffice. From the root folder, run:
```
docker-compose up
```

### then, open in your browser:
- Client: http://localhost:5050/login
- Backend (Django admin): http://localhost:8000/admin
- Backend (List transactions and users): http://localhost:8000/api/users/
- Backoffice: http://localhost:5150/transactions

