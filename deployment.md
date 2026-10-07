# Deployment Guide

This document outlines the standard deployment process for the Probash Mart Backend (Django).

## Server Details
- **Server:** Hetzner (`musa` alias in SSH config)
- **Deployment Path:** `/root/probash-mart-backend`
- **Docker Container Name:** `probash-mart-backend`
- **Port:** Maps `8003 -> 8000` internally.

## Deployment Steps

1. **Sync Changes to the Server**
   From your local machine, run the following `rsync` command to safely upload only the changed Python files (excluding virtual environments, caches, and SQLite databases):
   ```bash
   rsync -avz --exclude '__pycache__' --exclude 'venv' --exclude '*.sqlite3' --exclude '.git' /Users/mehedihasanmridul/Backend/Probash-Mart-Backend/ musa:/root/probash-mart-backend/
   ```

2. **Rebuild and Restart the Docker Container**
   SSH into the server, navigate to the project directory, rebuild the image (if you added new dependencies), and restart the container.
   ```bash
   ssh musa
   cd /root/probash-mart-backend
   docker compose build
   docker compose up -d
   ```
   *Note: If you only changed Python code and didn't add new packages, you can simply run `docker compose restart` without rebuilding.*

3. **Database Migrations & Collectstatic**
   If you made changes to `models.py` or static files, you must run migrations inside the container:
   ```bash
   docker exec -it probash-mart-backend python manage.py migrate
   docker exec -it probash-mart-backend python manage.py collectstatic --noinput
   ```

4. **Verify Deployment**
   Check the logs to ensure Gunicorn/Django has started without errors:
   ```bash
   docker logs -f probash-mart-backend
   ```
