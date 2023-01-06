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

# Create books
echo "Create book 1"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "2266274287", "title":"Les misérables", "authors":[1]}' http://127.0.0.1:8000/books; echo
echo "Create book 2"
curl -X POST -H "Content-Type: application/json" -d '{"isbn": "9782710810025", "title":"Shared Earth Modeling", "authors":[3, 4]}' http://127.0.0.1:8000/books; echo



