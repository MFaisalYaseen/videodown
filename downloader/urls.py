from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/formats/', views.api_formats, name='api_formats'),
    path('api/download/', views.api_download, name='api_download'),
    path('get/<str:file_id>/<str:ext>/', views.serve_file, name='serve_file'),
    path('robots.txt', views.robots_txt),
    path('sitemap.xml', views.sitemap_xml),
    path('tiktok-downloader/', views.platform_page, {'slug': 'tiktok-downloader'}, name='tiktok'),
    path('instagram-downloader/', views.platform_page, {'slug': 'instagram-downloader'}, name='instagram'),
    path('youtube-downloader/', views.platform_page, {'slug': 'youtube-downloader'}, name='youtube'),
    path('facebook-downloader/', views.platform_page, {'slug': 'facebook-downloader'}, name='facebook'),
    path('twitter-downloader/', views.platform_page, {'slug': 'twitter-downloader'}, name='twitter'),
]