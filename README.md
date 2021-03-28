## Install instruction
```
Create .env file

MYSQL_DATABASE={}
MYSQL_USER={}
MYSQL_PASSWORD={}
MYSQL_ROOT_PASSWORD={}
SECRET_KEY={}
```
```
docker-compose up -d --build
```

## Basic methods

### GET /
Home page with all link user rules and a form for adding new ones

### POST /
Adding a new link rule

### GET /r/<short_link>/
Redirect to the original link of the specified {subpart}