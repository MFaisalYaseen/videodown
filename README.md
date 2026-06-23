# VidDown — Video Downloader Website

## Local testing
```bash
pip install -r requirements.txt
DEBUG=True python manage.py runserver
```
Open: http://127.0.0.1:8000

## VPS Deployment
1. Upload code to VPS
2. Run: bash deploy.sh
3. Edit /var/www/videodown/.env with your domain
4. Change yoursite.com in deploy.sh to your real domain

## SEO Checklist
- [ ] Replace "yoursite.com" in sitemap_xml view with real domain
- [ ] Replace "yoursite.com" in base.html canonical tags
- [ ] Submit sitemap to Google Search Console
- [ ] Add Google Analytics
- [ ] Apply for Google AdSense after 1000 daily visitors

## Earning Setup
- AdSense: Add ad code in base.html <head> after approval
- Replace "VidDown.pro" logo with your brand name
