#!/bin/bash
# Create authors
echo "Create author 1"
curl -X POST -H "Content-Type: application/json" -d '{"name":"Victor HugO"}' http://127.0.0.1:8000/authors; echo
echo "Create author 2"
curl -X POST -H "Content-Type: application/json" -d '{"name":"Boris Vian"}' http://127.0.0.1:8000/authors; echo
echo "Create author 3"
curl -X POST -H "Content-Type: application/json" -d '{"name":"Jean-Francois Rainaud"}' http://127.0.0.1:8000/authors; echo
echo "Create author 4"
curl -X POST -H "Content-Type: application/json" -d '{"name":"Michel Perrin"}' http://127.0.0.1:8000/authors; echo

echo "Update author 1"
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Victor Hugo"}' http://127.0.0.1:8000/authors/1; echo
echo "Create author 5"
curl -X POST -H "Content-Type: application/json" -d '{"name":"Auteur à virer"}' http://127.0.0.1:8000/authors; echo
echo "Delete author 5"
curl -X DELETE -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/authors/5; echo

echo "Get all authors"
curl -X GET -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/authors; echo
echo "Get author 1"
curl -X GET -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/authors/1; echo


# Create books
echo
echo "Create book 1"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "2266274287", "title":"Les misérables", "authors":[1]}' http://127.0.0.1:8000/books; echo
echo "Create book 2"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "2302031474", "title":"Notre Dame de Paris", "authors":[1]}' http://127.0.0.1:8000/books; echo
echo "Create book 3"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "9782710810025", "title":"Shared Earth Modeling", "authors":[3, 4]}' http://127.0.0.1:8000/books; echo

echo "Create book 4"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "1782710810025", "title":"Shared Earth Modeling 2", "authors":[3, 4]}' http://127.0.0.1:8000/books; echo
echo "Update book 4"
curl -X PUT -H "Content-Type: application/json" -d '{"isbn": "1782710810025", "title":"Shared Earth Modeling 9", "authors":[1, 4]}' http://127.0.0.1:8000/books/4; echo
echo "Delete book 4"
curl -X DELETE -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/books/4; echo

# Create Copy
echo "Create copy 1"
curl -X POST -H "Content-Type: application/json" -d '{"place":"R1E1", "book_id":1}' http://127.0.0.1:8000/copies; echo
# Create Copy
echo "Create copy 2"
curl -X POST -H "Content-Type: application/json" -d '{"place":"R1E1", "book_id":1}' http://127.0.0.1:8000/copies; echo
# Create Copy
echo "Create copy 3"
curl -X POST -H "Content-Type: application/json" -d '{"place":"R1E1", "book_id":1}' http://127.0.0.1:8000/copies; echo
# Create Copy
echo "Create copy 4"
curl -X POST -H "Content-Type: application/json" -d '{"place":"R1E1", "book_id":2}' http://127.0.0.1:8000/copies; echo
# Create copy
echo "Create copy 5"
curl -X POST -H "Content-Type: application/json" -d '{"place":"R1E1", "book_id":2}' http://127.0.0.1:8000/copies; echo
# Patch copy 4
echo "Patch copy 4"
curl -X PATCH -H "Content-Type: application/json" -d '{"place":"R2E2", "book_id":2}' http://127.0.0.1:8000/copies/4; echo
# Get copy 4
echo "Get copy 4"
curl -X GET -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/copies/4; echo
# Delete copy 5
echo "Delete copy 5"
curl -X DELETE -H "Content-Type: application/json" -d '' http://127.0.0.1:8000/copies/5; echo

# Create checkouts
echo "Create checkout 1"
curl -X POST -H "Content-Type: application/json" -d '{"borrower":"Gédéon", "copy_id":1}' http://127.0.0.1:8000/checkouts; echo
