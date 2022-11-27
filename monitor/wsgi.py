from monitor.app import app


def application(*args, **kwargs):
    """
    Starts the appplication via a wsgi http server. Examples:
      uwsgi -p 4 --http-socket 127.0.0.15000 -H ~/.virtualenvs/sauron -w locus_sauron.restapp.wsgi
      gunicorn -w 4 -b 127.0.0.1:5000 locus_sauron.restapp.wsgi
    """

    return app(*args, **kwargs)
