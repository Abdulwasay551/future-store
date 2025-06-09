from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    path('checkout/', views.checkout, name='checkout'),
    path('address/add/', views.add_address, name='add_address'),
    path('order/place/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/history/', views.order_history, name='order_hist'),
    path('review/<int:review_id>/', views.get_review, name='get_review'),
    path('product/<int:product_id>/reviews/', views.load_more_reviews, name='load_more_reviews'),
]
