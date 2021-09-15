# DRF Library API

This application is an API built with Django REST Framework (DRF) that lets users track books that they want to read or are reading -- kind of like GoodReads. Books are listed with important information like title, author, publication date, and whether it is marked as “featured”.

Any logged-in user can add a new book as long as the same book is not already in the library. Only admin users can update book details (like marking it as featured) or delete books.

Books are be unique by title and author (that is, you can’t have two books with the same title and author; two books with the same title is fine as long as the authors are different).

Users can mark a book as “want to read”, “reading”, or “read/done”.

Users can also write reviews on books, which should be viewable to all users. Optionally, users can take private notes on books.

**All requests require authentication**.

## Required Headers

Requests to endpoints requiring authentication should set the `Authorization` header to `Token <token>`, where `<token>` is the token received in the login response.

POST requests with a body should set the `Content-Type` header to `application/json`.

## Log In

### request

```txt
POST auth/login

{
	"username": "admin",
	"password": "admin"
}
```

### response

```json
{
  "auth_token": "c312049c7f034a3d1b52eabc2040b46e094ff34c"
}
```

## List all books

Requires authentication.

### request

```txt
GET api/books
```

### response

```json
[
  {
    "pk": 1,
    "title": "Paradise Lost",
    "author": "John Milton",
    "featured": true
  },
  {
    "pk": 2,
    "title": "The Countess of Pembroke's Arcadia",
    "author": "Philip Sidney",
    "featured": false
  },
  {
    "pk": 3,
    "title": "The Faerie Queene",
    "author": "Edmund Spenser",
    "featured": false
  }
]
```

## List all featured books

Requires authentication.

### request

```txt
GET api/books/featured
```

### response

```json
[
  {
    "pk": 1,
    "title": "Paradise Lost",
    "author": "John Milton",
    "publication_year": 1667,
    "featured": true,
    "reviews": [
      "http://127.0.0.1:8000/api/book_reviews/1"
    ]
  }
]
```

## Details for a single book

Requires authentication.

### request

```txt
GET api/books/{id}
```

### response

```json
[
  {
    "pk": 1,
    "title": "Paradise Lost",
    "author": "John Milton",
    "featured": true
  }
]
```

## Create a new book

Requires authentication.

### request

`title` and `author` are required fields.

```json
POST api/books

{
   "title": "The Anatomy of Melancholy",
   "author": "Robert Burton",
   "publication_year": 1621
}
```

### response

```json
201 Created
{
  "pk": 6,
  "title": "The Anatomy of Melancholy",
  "author": "Robert Burton",
  "publication_year": 1621,
  "featured": false,
  "reviews": []
}

```

## Update a book

Requires authentication. Available only to admin users.

### request

```txt

PATCH api/books/{id}

{
  "featured": true
}
```

### response

```json
200 OK

{
  "pk": 6,
  "title": "The Anatomy of Melancholy",
  "author": "Robert Burton",
  "publication_year": 1621,
  "featured": true,
  "reviews": []
}
```
