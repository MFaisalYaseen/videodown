import os, uuid, json
import yt_dlp
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

DOWNLOAD_DIR = '/tmp/videodown/'

PLATFORMS = {
    'tiktok': {
        'name': 'TikTok',
        'slug': 'tiktok-downloader',
        'icon': 'tiktok',
        'color': '#fe2c55',
        'gradient': 'linear-gradient(135deg,#010101 0%,#fe2c55 100%)',
        'title': 'TikTok Video Downloader — No Watermark Free HD',
        'h1': 'TikTok Video Downloader',
        'tagline': 'Download TikTok videos without watermark in HD. Free, fast, no app needed.',
        'meta_desc': 'Download TikTok videos without watermark for free. Save TikTok videos in HD MP4. Fast, free, no registration. Works on mobile and desktop.',
        'placeholder': 'Paste TikTok link here... https://www.tiktok.com/@user/video/123...',
        'domains': ['tiktok.com', 'vm.tiktok.com'],
        'how_to': [
            ('Open TikTok', 'Find the video you want to download in the TikTok app or website'),
            ('Copy Link', 'Tap Share button then tap "Copy Link" on the video'),
            ('Paste & Download', 'Paste the link in the box above and click the Download button'),
        ],
        'features': [
            ('No Watermark', 'Get clean videos without TikTok logo', 'shield-check'),
            ('HD Quality', 'Download in original high definition quality', 'hd'),
            ('100% Free', 'No registration, no limits, always free', 'currency-dollar'),
            ('Fast & Secure', 'Your link is never stored on our servers', 'bolt'),
        ],
        'faq': [
            ('How to download TikTok video without watermark?', 'Paste your TikTok video URL in the box above and click Download. Our tool automatically removes the TikTok watermark and gives you a clean HD video file.'),
            ('Is this TikTok downloader free?', 'Yes, 100% free. No registration needed, no hidden fees, no daily limits. Download as many TikTok videos as you want.'),
            ('Can I download TikTok videos on iPhone?', 'Yes! Open Safari on your iPhone, paste the TikTok link above, click Download and save the video to your Photos app.'),
            ('What format will the video be in?', 'Videos download in MP4 format which works on all devices — iPhone, Android, Windows PC, Mac and Smart TVs.'),
            ('How to download TikTok without the app?', 'You do not need the TikTok app. Just copy the video link from any browser and paste it above to download.'),
        ],
    },
    'instagram': {
        'name': 'Instagram',
        'slug': 'instagram-downloader',
        'icon': 'instagram',
        'color': '#e1306c',
        'gradient': 'linear-gradient(135deg,#405de6,#5851db,#833ab4,#c13584,#e1306c,#fd1d1d)',
        'title': 'Instagram Reels Downloader — Free HD Video & Photos',
        'h1': 'Instagram Video & Reels Downloader',
        'tagline': 'Download Instagram Reels, Videos and Stories in HD. No login required.',
        'meta_desc': 'Download Instagram Reels, videos and stories for free in HD quality. Save Instagram videos online without login. Fast and free Instagram downloader.',
        'placeholder': 'Paste Instagram Reel or video link... https://www.instagram.com/reel/...',
        'domains': ['instagram.com'],
        'how_to': [
            ('Open Instagram', 'Find the Reel, video or story you want to save'),
            ('Copy Link', 'Tap the 3 dots (...) on the post, then tap "Copy Link"'),
            ('Paste & Download', 'Paste the link above and hit the Download button'),
        ],
        'features': [
            ('Reels Download', 'Download Instagram Reels in full HD quality', 'player-play'),
            ('Stories Saver', 'Save Instagram Stories before they disappear', 'clock'),
            ('No Login', 'No Instagram account required to download', 'lock-open'),
            ('Photos Too', 'Download Instagram photos and carousels', 'photo'),
        ],
        'faq': [
            ('How to download Instagram Reels?', 'Copy the Instagram Reel link by tapping the 3-dot menu and selecting Copy Link. Then paste it in the box above and click Download.'),
            ('Can I download Instagram Stories?', 'Yes! Paste any public Instagram Story link above to download it instantly. Stories are downloaded before they expire.'),
            ('Do I need to log in to my Instagram?', 'No login required for public videos, Reels and posts. Simply paste the link and download.'),
            ('What quality are the downloaded Instagram videos?', 'We download in the highest available quality, usually 1080p HD. Quality depends on the original upload.'),
            ('Why is my Instagram video not downloading?', 'Make sure the account is public. Private account content cannot be downloaded. Also check the link is correct.'),
        ],
    },
    'youtube': {
        'name': 'YouTube',
        'slug': 'youtube-downloader',
        'icon': 'youtube',
        'color': '#ff0000',
        'gradient': 'linear-gradient(135deg,#282828 0%,#ff0000 100%)',
        'title': 'YouTube Video Downloader MP4 — Free HD 1080p & 4K',
        'h1': 'YouTube Video Downloader',
        'tagline': 'Download YouTube videos in MP4 HD and 4K. Convert to MP3 audio. Totally free.',
        'meta_desc': 'Download YouTube videos in MP4 format free. Save YouTube videos in HD 1080p and 4K. Convert YouTube to MP3. Fast YouTube video downloader online.',
        'placeholder': 'Paste YouTube video link... https://www.youtube.com/watch?v=...',
        'domains': ['youtube.com', 'youtu.be'],
        'how_to': [
            ('Open YouTube', 'Go to YouTube and find the video you want to download'),
            ('Copy URL', 'Copy the video URL from your browser address bar or tap Share then Copy Link'),
            ('Download', 'Paste the URL above, select your quality preference and click Download'),
        ],
        'features': [
            ('MP4 & MP3', 'Download as video or extract audio only', 'music'),
            ('4K Quality', 'Save videos up to 4K Ultra HD resolution', 'stars'),
            ('No Signup', 'No account needed, download instantly', 'user-off'),
            ('Fast Speed', 'High speed servers for quick downloads', 'rocket'),
        ],
        'faq': [
            ('How to download YouTube videos for free?', 'Paste the YouTube video URL in the box above, select your preferred quality (HD 1080p, 4K or MP3 audio), and click Download.'),
            ('Can I download YouTube videos in 4K?', 'Yes! If the original YouTube video is available in 4K, you can download it in 4K Ultra HD using our tool.'),
            ('How to convert YouTube to MP3?', 'Paste the YouTube link above, and we will automatically give you the best available video format. For audio, select MP3 option.'),
            ('Is it safe to download YouTube videos?', 'Our tool only fetches video from YouTube servers. We do not store your video files and we do not track your downloads.'),
            ('Can I download YouTube Shorts?', 'Yes! YouTube Shorts links work perfectly. Just paste the Shorts URL and download in seconds.'),
        ],
    },
    'facebook': {
        'name': 'Facebook',
        'slug': 'facebook-downloader',
        'icon': 'facebook',
        'color': '#1877f2',
        'gradient': 'linear-gradient(135deg,#0668E1 0%,#1877f2 100%)',
        'title': 'Facebook Video Downloader — HD & SD Free Download',
        'h1': 'Facebook Video Downloader',
        'tagline': 'Download Facebook videos and Reels in HD instantly. Free, no software needed.',
        'meta_desc': 'Download Facebook videos free in HD quality. Save Facebook Reels and public videos online. Fast Facebook video downloader, no software needed.',
        'placeholder': 'Paste Facebook video link... https://www.facebook.com/watch?v=...',
        'domains': ['facebook.com', 'fb.watch'],
        'how_to': [
            ('Find Video', 'Go to Facebook and find the video you want to save'),
            ('Copy Link', 'Click the 3 dots on the video post and select "Copy link"'),
            ('Download', 'Paste the link in the box above and click Download'),
        ],
        'features': [
            ('HD Quality', 'Download Facebook videos in HD 720p/1080p', 'hd'),
            ('FB Reels', 'Save Facebook Reels easily', 'player-play'),
            ('Fast Download', 'Download starts immediately, no waiting', 'bolt'),
            ('All Devices', 'Works on iPhone, Android, PC and Mac', 'devices'),
        ],
        'faq': [
            ('How to download Facebook videos?', 'Copy the Facebook video link by clicking the 3-dot menu on the video post, paste it above, and click Download to save in HD or SD.'),
            ('Can I download Facebook Reels?', 'Yes! Facebook Reels download is fully supported. Just paste the Facebook Reels URL in the box above.'),
            ('Why can I not download private Facebook videos?', 'Only public Facebook videos can be downloaded. Private and friends-only videos are protected and cannot be accessed.'),
            ('Does this work on mobile phones?', 'Yes, our Facebook video downloader works perfectly on iPhone, Android, iPad and all mobile browsers.'),
            ('What is the difference between HD and SD download?', 'HD is higher quality at 720p or 1080p resolution. SD is smaller file size at 360p or 480p. HD recommended for best quality.'),
        ],
    },
    'twitter': {
        'name': 'Twitter / X',
        'slug': 'twitter-downloader',
        'icon': 'brand-x',
        'color': '#000000',
        'gradient': 'linear-gradient(135deg,#14171A 0%,#657786 100%)',
        'title': 'Twitter / X Video Downloader — Free HD Download',
        'h1': 'Twitter & X Video Downloader',
        'tagline': 'Download videos from Twitter and X.com in HD quality. Free and instant.',
        'meta_desc': 'Download Twitter and X videos for free in HD quality. Save videos from Twitter tweets instantly. Fast and free Twitter video downloader online.',
        'placeholder': 'Paste Twitter / X tweet link... https://twitter.com/user/status/...',
        'domains': ['twitter.com', 'x.com'],
        'how_to': [
            ('Find Tweet', 'Find the tweet on Twitter or X.com that has the video'),
            ('Copy Link', 'Click Share and then "Copy link to Tweet"'),
            ('Download', 'Paste the tweet link above and click Download'),
        ],
        'features': [
            ('Twitter & X', 'Supports both twitter.com and x.com links', 'link'),
            ('HD Video', 'Download in the highest available quality', 'stars'),
            ('GIF Support', 'Download Twitter GIFs as MP4 files', 'gif'),
            ('Instant', 'Video ready to download in seconds', 'bolt'),
        ],
        'faq': [
            ('How to download Twitter videos?', 'Copy the tweet URL that contains the video from twitter.com or x.com, paste it in the box above, and click Download.'),
            ('Does it work with X.com links?', 'Yes! Both twitter.com and the new x.com links are fully supported. Just paste any tweet URL.'),
            ('Can I download Twitter GIFs?', 'Yes, Twitter GIFs can be downloaded as MP4 video files using our tool.'),
            ('Why is my Twitter video not downloading?', 'Make sure the tweet is from a public account. Tweets from protected (private) accounts cannot be downloaded.'),
            ('What video quality is available?', 'We download the highest available quality which is usually 720p or 1080p depending on what was originally uploaded.'),
        ],
    },
}

def get_platform_from_url(url):
    url_lower = url.lower()
    if 'tiktok.com' in url_lower or 'vm.tiktok.com' in url_lower:
        return 'tiktok'
    elif 'instagram.com' in url_lower:
        return 'instagram'
    elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'facebook'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'twitter'
    elif 'snapchat.com' in url_lower:
        return 'snapchat'
    elif 'pinterest.com' in url_lower or 'pin.it' in url_lower:
        return 'pinterest'
    elif 'dailymotion.com' in url_lower or 'dai.ly' in url_lower:
        return 'dailymotion'
    elif 'vimeo.com' in url_lower:
        return 'vimeo'
    return None

def home(request):
    ctx = {
        'page_title': 'Free Video Downloader — TikTok, Instagram, YouTube, Facebook, Twitter',
        'meta_desc': 'Download videos from TikTok, Instagram, YouTube, Facebook and Twitter for free. No watermark, HD quality, no registration required. Fast online video downloader.',
        'platforms': PLATFORMS,
        'is_home': True,
        'stats': [
            ('50M+', 'Videos Downloaded'),
            ('5 Platforms', 'Supported'),
            ('100%', 'Free Forever'),
            ('4K HD', 'Max Quality'),
        ],
    }
    return render(request, 'downloader/home.html', ctx)

def platform_page(request, slug):
    platform = None
    for key, val in PLATFORMS.items():
        if val['slug'] == slug:
            platform = key
            break
    if not platform:
        raise Http404
    cfg = PLATFORMS[platform]
    ctx = {
        'page_title': cfg['title'],
        'meta_desc': cfg['meta_desc'],
        'platform': platform,
        'cfg': cfg,
        'platforms': PLATFORMS,
        'is_home': False,
        'other_platforms': {k: v for k, v in PLATFORMS.items() if k != platform},
    }
    return render(request, 'downloader/platform.html', ctx)

@csrf_exempt
@require_POST
def api_formats(request):
    """Step 1 — fetch available qualities without downloading"""
    import urllib.parse as _up
    url = request.POST.get('url', '').strip()
    if not url or not url.startswith('http'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)

    _qs = _up.parse_qs(_up.urlparse(url).query)
    if 'list' in _qs or 'start_radio' in _qs:
        _v = _qs.get('v', [None])[0]
        if _v:
            url = f'https://www.youtube.com/watch?v={_v}'
        else:
            return JsonResponse({'error': 'Playlist links not supported. Paste a single video link.'}, status=400)

    platform = get_platform_from_url(url)
    if not platform:
        return JsonResponse({'error': 'Platform not supported.'}, status=400)

    TIKTOK_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    ydl_opts = {
        'quiet': True, 'no_warnings': True,
        'socket_timeout': 20, 'noplaylist': True,
        'nocheckcertificate': True,
        'http_headers': TIKTOK_HEADERS if platform == 'tiktok' else {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title     = info.get('title', '') or info.get('description', '') or 'TikTok Video'
        # Clean title - remove excessive hashtags if title is just hashtags
        if title and title.startswith('#'):
            desc = info.get('description', '')
            if desc:
                title = desc[:80]
            else:
                title = 'TikTok Video'
        title = title[:100]
        thumbnail = info.get('thumbnail', '') or ''
        duration  = info.get('duration', 0) or 0

        if duration > 1800:
            return JsonResponse({'error': 'Video is too long (max 30 min).'}, status=400)

        formats  = info.get('formats', [])
        qualities = []

        # ── TikTok: direct URL formats (fast, no-watermark) ──
        if platform == 'tiktok':
            for f in formats:
                fid = f.get('format_id', '')
                h   = f.get('height') or 0
                sz  = round((f.get('filesize') or f.get('filesize_approx') or 0) / (1024*1024), 1)
                # download_addr-0 = no watermark HD
                if fid == 'download_addr-0':
                    qualities.append({'format_id': fid, 'label': f'{h}p — No Watermark ✓' if h else 'HD — No Watermark ✓', 'height': h or 999, 'size_mb': sz, 'ext': 'mp4', 'type': 'video'})
                elif fid == 'download_addr-1':
                    qualities.append({'format_id': fid, 'label': f'{h}p — No Watermark', 'height': h or 998, 'size_mb': sz, 'ext': 'mp4', 'type': 'video'})
                elif fid == 'play_addr' and h:
                    qualities.append({'format_id': fid, 'label': f'{h}p Standard', 'height': h, 'size_mb': sz, 'ext': 'mp4', 'type': 'video'})
            if not qualities:
                qualities = [{'format_id': 'best', 'label': 'Best Available — No Watermark', 'height': 0, 'size_mb': 0, 'ext': 'mp4', 'type': 'video'}]
            qualities.sort(key=lambda x: x['height'], reverse=True)

        else:
            # ── YouTube / Instagram / Facebook / Twitter / others ──
            seen_heights = set()
            for f in reversed(formats):
                h      = f.get('height') or 0
                ext    = f.get('ext', '')
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                has_video = vcodec not in ('none', None, '')
                # Show ALL video formats — ffmpeg now installed so merging works
                if h and ext == 'mp4' and has_video and h not in seen_heights:
                    seen_heights.add(h)
                    sz = round((f.get('filesize') or f.get('filesize_approx') or 0) / (1024*1024), 1)
                    needs_merge = acodec in ('none', None, '')
                    if h >= 2160:   label = f'{h}p 4K Ultra HD'
                    elif h >= 1080: label = f'{h}p Full HD'
                    elif h >= 720:  label = f'{h}p HD'
                    else:           label = f'{h}p'
                    if needs_merge:
                        label += ' +'
                    qualities.append({
                        'format_id': f['format_id'],
                        'label': label,
                        'height': h,
                        'size_mb': sz,
                        'ext': 'mp4',
                        'type': 'video',
                        'needs_merge': needs_merge,
                    })

            qualities.sort(key=lambda x: x['height'], reverse=True)

            # MP3 for YouTube
            if platform == 'youtube':
                qualities.append({'format_id': 'bestaudio', 'label': 'MP3 — Audio Only 🎵', 'height': 0, 'size_mb': 0, 'ext': 'mp3', 'type': 'audio'})

            if not qualities:
                qualities = [{'format_id': 'best', 'label': 'Best Available', 'height': 0, 'size_mb': 0, 'ext': 'mp4', 'type': 'video'}]

        return JsonResponse({
            'success': True,
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'platform': platform,
            'clean_url': url,
            'qualities': qualities,
        })

    except Exception as e:
        return JsonResponse({'error': 'Could not fetch video info. Check the link and try again.'}, status=400)


@csrf_exempt
@require_POST
def api_download(request):
    import urllib.parse as _up
    url = request.POST.get('url', '').strip()
    format_id = request.POST.get('format_id', '').strip()
    fmt_type = request.POST.get('type', 'video').strip()

    if not url or not url.startswith('http'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)

    # Clean playlist URLs
    _qs = _up.parse_qs(_up.urlparse(url).query)
    if 'list' in _qs or 'start_radio' in _qs:
        _v = _qs.get('v', [None])[0]
        if _v:
            url = f'https://www.youtube.com/watch?v={_v}'
        else:
            return JsonResponse({'error': 'Playlist links not supported.'}, status=400)

    platform = get_platform_from_url(url)
    if not platform:
        return JsonResponse({'error': 'Platform not supported.'}, status=400)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    out_tpl  = os.path.join(DOWNLOAD_DIR, file_id + '.%(ext)s')

    # Pick format string — ffmpeg installed so merging is OK
    if fmt_type == 'audio':
        fmt_str = 'bestaudio[ext=m4a]/bestaudio/best'
    elif platform == 'tiktok':
        if format_id and format_id not in ('best',):
            fmt_str = f'{format_id}/download_addr-0/best'
        else:
            fmt_str = 'download_addr-0/download_addr-1/play_addr/best'
    elif format_id and format_id not in ('best', 'bestaudio'):
        # Merge selected video with best audio
        fmt_str = f'{format_id}+bestaudio[ext=m4a]/{format_id}+bestaudio/{format_id}/best[ext=mp4]/best'
    else:
        fmt_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'

    # TikTok needs special headers
    if platform == 'tiktok':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    ydl_opts = {
        'format': fmt_str,
        'outtmpl': out_tpl,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 60,
        'noplaylist': True,
        'nocheckcertificate': True,
        'http_headers': headers,
        'retries': 5,
        'fragment_retries': 5,
        'continuedl': True,
    }

    if fmt_type == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Single call — extract info AND download together (faster, one connection)
            info = ydl.extract_info(url, download=True)
            duration  = info.get('duration', 0) or 0
            title     = info.get('title', 'video')[:100]
            thumbnail = info.get('thumbnail', '')
            ext = 'mp3' if fmt_type == 'audio' else info.get('ext', 'mp4')

        # Find actual downloaded file
        actual = os.path.join(DOWNLOAD_DIR, f'{file_id}.{ext}')
        if not os.path.exists(actual):
            for f in os.listdir(DOWNLOAD_DIR):
                if f.startswith(file_id):
                    actual = os.path.join(DOWNLOAD_DIR, f)
                    ext = f.rsplit('.', 1)[-1]
                    break

        size_mb = round(os.path.getsize(actual) / (1024*1024), 1) if os.path.exists(actual) else 0

        return JsonResponse({
            'success': True,
            'title': title,
            'platform': platform,
            'file_id': file_id,
            'ext': ext,
            'thumbnail': thumbnail,
            'duration': duration,
            'size_mb': size_mb,
            'download_url': f'/get/{file_id}/{ext}/',
        })
    except yt_dlp.utils.DownloadError as e:
        msg = str(e).lower()
        if 'private' in msg:
            return JsonResponse({'error': 'This video is private.'}, status=400)
        if 'not available' in msg or 'unavailable' in msg:
            return JsonResponse({'error': 'Video not available or deleted.'}, status=400)
        if 'login' in msg or 'sign in' in msg:
            return JsonResponse({'error': 'This video requires login. Only public videos supported.'}, status=400)
        return JsonResponse({'error': 'Could not download. Check the link and try again.'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Something went wrong. Please try again.'}, status=500)

def serve_file(request, file_id, ext):
    safe_id = ''.join(c for c in file_id if c.isalnum() or c == '-')
    safe_ext = ''.join(c for c in ext if c.isalnum())
    filepath = os.path.join(DOWNLOAD_DIR, f'{safe_id}.{safe_ext}')
    if not os.path.exists(filepath):
        for f in os.listdir(DOWNLOAD_DIR):
            if f.startswith(safe_id):
                filepath = os.path.join(DOWNLOAD_DIR, f)
                break
        else:
            raise Http404
    resp = FileResponse(open(filepath, 'rb'), content_type='video/mp4')
    resp['Content-Disposition'] = f'attachment; filename="videodown.{safe_ext}"'
    return resp

def robots_txt(request):
    body = "User-agent: *\nAllow: /\nDisallow: /get/\nDisallow: /api/\n\nSitemap: https://yoursite.com/sitemap.xml"
    return HttpResponse(body, content_type='text/plain')

def sitemap_xml(request):
    from datetime import date
    today = date.today().isoformat()
    base = 'https://yoursite.com'
    pages = [
        ('/', '1.0'),
        ('/tiktok-downloader/', '0.9'),
        ('/instagram-downloader/', '0.9'),
        ('/youtube-downloader/', '0.9'),
        ('/facebook-downloader/', '0.9'),
        ('/twitter-downloader/', '0.9'),
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path, pri in pages:
        xml += f'  <url><loc>{base}{path}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>\n'
    xml += '</urlset>'
    return HttpResponse(xml, content_type='application/xml')