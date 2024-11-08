from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Author, Publisher, TitleAuthor, Title

def accueil(request):
    author_count = Author.objects.count()
    publisher_count = Publisher.objects.count()
    context = {
        'active_nav': 'accueil',
        'author_count': author_count,
        'publisher_count': publisher_count,
        'book_count': Title.objects.count() 
    }
    
    return render(request, template_name='registration/accueil.html', context=context)

def registration(request):
    return render(request, template_name='registration/registration.html', context={ 'active_nav':'registration'})

def author_detail(request, author_id):
    author = get_object_or_404(Author, au_id=author_id)
    return render(request, 'author/author_detail.html', {'author': author})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {'authors': authors, 'active_nav': 'author'})

#book views
def book_detail(request, isbn):  # utiliser isbn au lieu de book_id
    book = get_object_or_404(Title, isbn=isbn)
    return render(request, 'book/book_detail.html', {'book': book})

def book_list(request):
    objects = Title.objects.all().order_by('title')
    return render(request, template_name='book/book_list.html', context={'objects':objects, 'active_nav':'book'})


#publisher views
def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pubid=publisher_id)
    return render(request, 'publisher/publisher_detail.html', {'publisher': publisher})

def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'publisher/publisher_list.html', {'publishers': publishers, 'active_nav':'publisher'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie!")
            return redirect('accueil')
        else:
            messages.error(request, "Identifiants invalides.")
    
    return render(request, 'registration/login.html')