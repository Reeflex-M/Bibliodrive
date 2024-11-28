from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Author, Publisher, TitleAuthor, Title, ReservationHistory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.http import require_POST

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
    selected_genre = request.GET.get('genre', '')
    
    objects = Title.objects.all().order_by('title')
    if selected_genre:
        objects = objects.filter(genre=selected_genre)
    
    # Ajouter le nombre de réservations actives de l'utilisateur
    user_reservation_count = 0
    if request.user.is_authenticated:
        user_reservation_count = Title.get_active_reservations_count(request.user)
    
    context = {
        'objects': objects,
        'active_nav': 'book',
        'genres': Title.GENRE_CHOICES,
        'selected_genre': selected_genre,
        'user_reservation_count': user_reservation_count  # Nouvelle variable
    }
    return render(request, template_name='book/book_list.html', context=context)

@login_required
@require_POST
def reserve_book(request, isbn):
    try:
        book = get_object_or_404(Title, isbn=isbn)
        if book.reserve_by is None:
            active_reservations = Title.get_active_reservations_count(request.user)
            if active_reservations >= 3:
                return JsonResponse({
                    'success': False,
                    'message': "Vous ne pouvez pas réserver plus de 3 livres à la fois."
                })
                
            book.reserve_by = request.user
            book.save()
            ReservationHistory.objects.create(
                book=book,
                user=request.user,
                status='ACTIVE'
            )
            return JsonResponse({
                'success': True,
                'message': f"Le livre '{book.title}' a été réservé avec succès.",
                'newStatus': 'reserved',
                'reservedBy': request.user.username
            })
        return JsonResponse({
            'success': False,
            'message': "Ce livre est déjà réservé."
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@login_required
@require_POST
def cancel_reserve_book(request, isbn):
    book = get_object_or_404(Title, isbn=isbn)
    if book.reserve_by == request.user:
        book.reserve_by = None
        book.save()
        reservation = ReservationHistory.objects.filter(
            book=book,
            user=request.user,
            status='ACTIVE'
        ).first()
        if reservation:
            reservation.status = 'CANCELLED'
            reservation.cancelled_at = timezone.now()
            reservation.save()
        return JsonResponse({
            'success': True,
            'message': f"La réservation du livre '{book.title}' a été annulée.",
            'newStatus': 'available'
        })
    return JsonResponse({
        'success': False,
        'message': "Vous ne pouvez pas annuler cette réservation."
    })

@login_required
def book_historique(request):
    reservations = ReservationHistory.objects.all()
    context = {
        'reservations': reservations,
        'active_nav': 'historique'
    }
    
    if request.user.is_superuser:
        # Ajouter les livres disponibles et les utilisateurs au contexte
        context.update({
            'available_books': Title.objects.all(),
            'users': User.objects.all()
        })
    
    return render(request, 'book/book_historique.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_reservation(request):
    if request.method == 'POST':
        book = get_object_or_404(Title, isbn=request.POST.get('book'))
        user = get_object_or_404(User, id=request.POST.get('user'))
        
        ReservationHistory.objects.create(
            book=book,
            user=user,
            status='ACTIVE'
        )
        book.reserve_by = user
        book.save()
        
        messages.success(request, "Réservation ajoutée avec succès")
    return redirect('book_historique')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(ReservationHistory, id=reservation_id)
        if reservation.status == 'ACTIVE':
            book = reservation.book
            book.reserve_by = None
            book.save()
            # Au lieu de supprimer, on met à jour le statut
            reservation.status = 'ADMIN_CANCELLED'
            reservation.cancelled_at = timezone.now()
            reservation.save()
            messages.success(request, "Réservation annulée avec succès")
        else:
            messages.error(request, "Cette réservation est déjà terminée")
    return redirect('book_historique')

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