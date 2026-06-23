#!/bin/bash
# ============================
# VidDown VPS Deployment Script
# Run this on your Contabo VPS
# ============================

echo "=== VidDown Deployment ==="

# 1. Install system packages
sudo apt update && sudo apt install -y python3-pip python3-venv nginx

# 2. Create project folder
sudo mkdir -p /var/www/videodown
cd /var/www/videodown

# 3. Clone or upload your code here
# git clone https://github.com/youruser/videodown.git .

# 4. Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Setup .env file
cp .env.example .env
echo "EDIT .env file with your domain and secret key!"

# 6. Collect static files
DJANGO_SETTINGS_MODULE=core.settings python manage.py collectstatic --noinput

# 7. Create Gunicorn systemd service
sudo tee /etc/systemd/system/videodown.service << 'SERVICE'
[Unit]
Description=VidDown Gunicorn
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/videodown
EnvironmentFile=/var/www/videodown/.env
ExecStart=/var/www/videodown/venv/bin/gunicorn core.wsgi:application --workers 3 --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl enable videodown
sudo systemctl start videodown

# 8. Nginx config
sudo tee /etc/nginx/sites-available/videodown << 'NGINX'
server {
    listen 80;
    server_name yoursite.com www.yoursite.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/videodown/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /get/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/videodown /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 9. SSL with Certbot (free HTTPS)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yoursite.com -d www.yoursite.com

# 10. Auto cleanup old downloaded files (every hour)
(crontab -l 2>/dev/null; echo "0 * * * * find /tmp/videodown -mmin +60 -delete") | crontab -
# Auto update yt-dlp daily (important!)
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/videodown/venv/bin/pip install -U yt-dlp -q") | crontab -

echo "=== Deployment Complete! ==="
echo "Visit: http://yoursite.com"
