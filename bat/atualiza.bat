git pull origin main
docker compose exec django python manage.py migrate
docker compose restart