import multiprocessing
import os
name = "Gunicorn config for FastAPI"

log_file = "-"

bind = "0.0.0.0:80"
timeout = 2400

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1