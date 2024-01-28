"""gunicorn WSGI server configuration."""

from multiprocessing import cpu_count
from os import environ

# The address to bind to (e.g., "0.0.0.0:5000" or "unix:/tmp/gunicorn.sock")
bind = environ.get("BIND", "0.0.0.0:5000")

# The number of worker processes
workers = cpu_count() * 2 + 1

# The path to the access log file (set to "-" to disable logging)
accesslog = "-"

# The log file to write to (set to "-" to log to stdout)
errorlog = "gunicorn.log"

# The log level (debug, info, warning, error, critical)
loglevel = "warning"

# Worker class (options: sync, eventlet, gevent)
worker_class = "sync"
