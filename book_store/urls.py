from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_home, name='book_home'),
    path('search/', views.book_search, name='book_search'),
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('cart/', views.book_cart, name='book_cart'),
    path('checkout/', views.book_checkout, name='book_checkout'),
    path('weblog/', views.weblog_home, name='weblog_home'),
    path('weblog/<int:pk>/', views.weblog_detail, name='weblog_detail'),
    path('change-favorite-state/<int:pk>/', views.change_favorite_state, name='change_favorite_state'),
    path('dashboard-home/', views.dashboard_home, name='dashboard_home'),
    path('dashboard-blog/', views.dashboard_blog, name='dashboard_blog'),
    path('dashboard-blog-add/', views.dashboard_blog_add, name='dashboard_blog_add'),
    path('dashboard-blog-update/<int:pk>/', views.dashboard_blog_update, name='dashboard_blog_update'),
    path('dashboard-blog-delete/<int:pk>/', views.dashboard_blog_delete, name='dashboard_blog_delete'),
    path('dashboard-comment/', views.dashboard_comment, name='dashboard_comment'),
    path('dashboard-comment-delete/<int:pk>/', views.dashboard_comment_delete, name='dashboard_comment_delete'),
    path('dashboard-favorite/', views.dashboard_favorite, name='dashboard_favorite'),
    path('dashboard-update-profile/', views.dashboard_update_profile, name='dashboard_update_profile'),
    path('dashboard-order/', views.dashboard_order, name='dashboard_order'),
    path('dashboard-order-item/<int:pk>/', views.dashboard_order_item, name='dashboard_order_item'),
    path('dashboard-transaction/', views.dashboard_transaction, name='dashboard_transaction'),
    path('session/<int:pk>/<str:task>/', views.session, name='session'),
]
