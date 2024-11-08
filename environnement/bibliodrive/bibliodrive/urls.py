from django.contrib import admin
from django.urls import path
from backoffice import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil/', views.accueil, name="accueil"),
    path('login/', views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.accueil, name='accueil'),

    path('author/<int:author_id>', views.author_detail, name="author-detail"),
    path('authors/', views.author_list, name="author-list"),

    path('publisher/<int:publisher_id>', views.publisher_detail, name="publisher-detail"),
    path('publishers/', views.publisher_list, name="publisher-list"),

    path('book/<str:isbn>', views.book_detail, name="book-detail"),
    path('books/', views.book_list, name="book-list"),
    
    
    
]
