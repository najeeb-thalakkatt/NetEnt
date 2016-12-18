# NetEnt

## Problem Statement:
Using Django and Django REST Framework

Create the following two models

- Book
- Genre

Each book should have one author (you can use django's built in User).
Each book can have multiple Genres

Create an api to add new genres.
Create an api to create and update books (POST/PUT).

When creating a book, the author should automatically be selected based on the logged in user.
Only the author should be able to update his/her book, if the user does not have permission to update the response from the api should reflect this.
A book title has to be unique per author (each author can have a book with the same title, but an author can not have two books with the same title). 

Special case, lets consider this to be the free version of a site. In that case, an author is only allowed to have 5 books at one time.

## Technologies Used:
1. Python 2.7
2. Django
3. Django Rest Framework

## How To Run:
1. Clone the repository
2. cd NetEnt/book_app
3. Go to your virtual env
4. pip install -r requirements.txt
5. python manage.py syncdb
7. python manage.py runserver
8. Sever will be running in 127.0.0.1:8000 by default

## Api Document:

**Register a user :**

Request:

POST : http://127.0.0.1:8000/user/register

{
	"username": "alen",
	"password": "123456",
	"email": "naj@sdf.com"
}
Responses:

{
	"data": {
		"username": "alen2",
		"id": 7,
		"email": "naj@sdf.com"
	}
}

{
  "error": {
    "message": "User already exists"
  }
}

**Add a genre :**

Only super user can add new genres.

Request:

POST : http://127.0.0.1:8000/genre

username: najeeb
password: 123456

{
	"genres": ["comic", "horror", "sports"]
}

Responses:

Duplicate means the data already exists in database.

{
	"data": {
		"genre_duplicates": [
			"sports"
		],
		"genre_details": ["comic",
			"horror"
		]
	}
}

{
  "detail": "Invalid username/password."
}

{
  "error": {
    "message": "User is not authorized for the operation, Please use super user credentials"
  }
}

**Add a new book :**

Request:

POST : http://127.0.0.1:8000/book

username: alen
password: 123456

{
	"books": [{
		"title": "Mid Night Children",
		"genres": ["Fantasy", "Sci-Fi"]
	}, {
		"title": "Rebel",
		"genres": ["History"]
	}]
}

Responses:

Duplicate data means this book is already added.
{
	"duplicate_data": [{
		"genres": [
			"History"
		],
		"title": "Rebel"
	}],
	"data": [{
		"genres": [
			"Fantasy",
			"Sci-Fi"
		],
		"title": "Mid Night Children"
	}]
}

{
  "detail": "Invalid username/password."
}

{
  "error": {
    "message": "You have covered free quota"
  }
}

**Edit a book :**

Request:

PUT : http://127.0.0.1:8000/book

username: alen
password: 123456


{
	"book_title": "New Title",
	"genres": ["Fantasy", "Sci-Fi","New4"],
	"id":17
}

Responses:

{
	"book_title": "New Title",
	"genres": [
		"Fantasy",
		"Sci-Fi",
		"New4"
	],
	"id": 17
}

{
  "error": {
    "message": "You are not the author of the book"
  }
}

**Get a book :**

Request:
Get : http://127.0.0.1:8000/book/{id}

username: alen
password: 123456

Responses:

{
	"title": "New Title",
	"id": 9,
	"author": "new_user1",
	"genres": [{
		"genre_str": "Fantasy",
		"id": 6
	}, {
		"genre_str": "Sci-Fi",
		"id": 7
	}, {
		"genre_str": "History",
		"id": 8
	}, {
		"genre_str": "New4",
		"id": 12
	}]

}

{
  "error": {
    "message": "Book not found"
  }
}

{
  "error": {
    "message": "You are not the author of the book"
  }
}

