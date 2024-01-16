cd ./ProfileWeb
gunicorn -w 2 server:app -b 0.0.0.0:5000