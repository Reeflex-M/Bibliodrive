from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Author, Publisher, TitleAuthor, Title
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json

#accueil views
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


#registration views
def registration(request):
    return render(request, template_name='registration/registration.html', context={ 'active_nav':'registration'})


@csrf_exempt  # Désactive la protection CSRF pour cette vue
def register_view(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            form = UserCreationForm({
                'username': data.get('username'),
                'password1': data.get('password1'),
                'password2': data.get('password2')
            })
        else:
            form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.content_type == 'application/json':
                return JsonResponse({
                    "success": True,
                    "message": "Inscription réussie!",
                    "username": user.username,
                    "redirect": "/accueil/"
                })
            return redirect('accueil')
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'active_nav': 'register'
    }
    return render(request, 'registration/register.html', context)


#author views
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

@login_required
def reserve_book(request, isbn):
    book = get_object_or_404(Title, isbn=isbn)
    if book.reserve_by is None:
        book.reserve_by = request.user
        book.save()
        messages.success(request, f"Le livre '{book.title}' a été réservé avec succès.")
    else:
        messages.error(request, "Ce livre est déjà réservé.")
    return redirect('book-list')

@login_required
def cancel_reserve_book(request, isbn):
    book = get_object_or_404(Title, isbn=isbn)
    if book.reserve_by == request.user:
        book.reserve_by = None
        book.save()
        messages.success(request, f"La réservation du livre '{book.title}' a été annulée.")
    else:
        messages.error(request, "Vous ne pouvez pas annuler cette réservation.")
    return redirect('book-list')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def book_historique(request):
    return render(request, 'book/book_historique.html')

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