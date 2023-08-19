"""gunicorn WSGI server configuration."""

from multiprocessing import cpu_count
from os import environ

# Gunicorn configuration file

# The address to bind to (e.g., "0.0.0.0:5000" or "unix:/tmp/gunicorn.sock")
bind = environ.get('BIND', '0.0.0.0:5000')

# The number of worker processes
workers = cpu_count() + 1
# workers = cpu_count() * 2 + 1  # for production

# The number of threads per worker process
threads = 2  

# The maximum number of simultaneous clients that a worker can handle
worker_connections = 1000

# The maximum number of requests a worker will process before restarting
max_requests = 1000

# The maximum number of requests a worker will process before reloading the application code
max_requests_jitter = 50

# The timeout for graceful worker shutdown
timeout = 120

# The number of seconds to wait for the next request on a keep-alive connection
# keepalive = 2

# The maximum number of seconds a worker can be idle before being terminated
# Set to 0 to disable worker timeout
#worker_timeout = 60

# The maximum number of seconds to wait for the upstream server response
#proxy_read_timeout = 300

# The maximum number of seconds to wait for a request body from the client
#proxy_send_timeout = 300

# The maximum size of request body
#limit_request_line = 4094
#limit_request_fields = 100
#limit_request_field_size = 8190

# The path to the access log file (set to "-" to disable logging)
accesslog = "-"

# The log level (debug, info, warning, error, critical)
loglevel = "warning"

# The log file to write to (set to "-" to log to stdout)
logfile = "gunicorn.log"

# The worker class
worker_class = "sync"

# The path to the SSL certificate file
#certfile = "/path/to/cert.pem"

# The path to the SSL private key file
#keyfile = "/path/to/key.pem"

# The number of seconds for the web server to gracefully shutdown
#graceful_timeout = 30
