from django.urls import path
from . import views

app_name = 'cms_store'

urlpatterns = [
    # Blog URLs
    path('blog/', views.blog_index, name='blog_index'),
    path('blog/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('blog/category/<slug:slug>/', views.blog_category, name='blog_category'),
    path('blog/tag/<slug:slug>/', views.blog_tag, name='blog_tag'),
]