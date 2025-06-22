from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test_view'),
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/product/<int:product_id>/color/<int:color_id>/images/', views.get_color_images, name='get_color_images'),
    path('api/product/<int:product_id>/colors/', views.get_product_colors, name='get_product_colors'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-address/', views.add_address, name='add_address'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
    path('get-review/<int:review_id>/', views.get_review, name='get_review'),
    path('load-more-reviews/<int:product_id>/', views.load_more_reviews, name='load_more_reviews'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-notifications-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('test-colors/', views.test_colors, name='test_colors'),
]
