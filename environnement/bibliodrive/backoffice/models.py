from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    au_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50)
    year_born = models.SmallIntegerField()

    def __str__(self):
        return self.author


class Publisher(models.Model):
    pubid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    comments = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.company_name}"


class TitleAuthor(models.Model):
    isbn = models.CharField(max_length=20, primary_key=True)
    au_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['isbn', 'au_id'], name='unique_title_author')
        ]

    def __str__(self):
        return f"{self.isbn} - {self.au_id.author}"

class Title(models.Model):
    title = models.CharField(max_length=255)
    year_published = models.SmallIntegerField()
    isbn = models.CharField(max_length=20, primary_key=True)
    pubid = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    reserve_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    comments = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    GENRE_CHOICES = [
        ('ROMAN', 'Roman'),
        ('SCIENCE', 'Science'),
        ('HISTOIRE', 'Histoire'),
        ('POLICIER', 'Policier'),
        ('FANTASY', 'Fantasy'),
        ('BIOGRAPHIE', 'Biographie'),
        ('AUTRE', 'Autre'),
    ]
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='AUTRE')

    def __str__(self):
        return self.title

class ReservationHistory(models.Model):
    book = models.ForeignKey(Title, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Annulée'),
        ('ADMIN_CANCELLED', 'Annulée par admin')  # Nouveau statut
    ])

    class Meta:
        ordering = ['-reserved_at']

    def __str__(self):
        return f"{self.book.title} - {self.user.username} - {self.status}"
