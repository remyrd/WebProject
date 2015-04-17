web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker manage:app -w 1
init: python db_create.py
