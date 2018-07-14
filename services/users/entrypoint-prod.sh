#! /bin/sh

echo "Waiting for postress...."

while ! nc -z users-db 5432; do
  sleep 0.1
done

echo "Postrges sql started .."

gunicorn -b 0.0.0.0:5000 manage:app
