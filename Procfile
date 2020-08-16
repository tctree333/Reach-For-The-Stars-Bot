web: gunicorn web:app -w 3 -t 300
bot: python3 main.py
celery: python3 worker.py
beat: python3 worker_sched.py
