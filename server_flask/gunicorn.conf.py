"""Gunicorn config file."""

# Number of worker processes
workers = 4

# Type of worker process (sync, eventlet, gevent, tornado, gthread)
worker_class = "sync"

# Address and port to bind to
bind = "127.0.0.1:5000"

# Timeout for workers (in seconds)
timeout = 30

# Log level (debug, info, warning, error, critical)
loglevel = "warning"

# Path to access log file
accesslog = "-"  # '-' means stdout

# Path to error log file
errorlog = "-"  # '-' means stderr

# Name of the application (for process titles)
proc_name = "staffsec"

# Daemonize the Gunicorn process
daemon = False

# Reload workers when code changes (for development)
reload = False
