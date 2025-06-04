# Tiny Bank
## Done by Fabricio + Holly + students of the fullstack-s25

## Running the backend:
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
```
docker-compose up
```

### then, open in your browser:
http://localhost:8000/api/users
http://localhost:8000/admin