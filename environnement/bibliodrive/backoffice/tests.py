from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from backoffice.models import Author, Publisher, Title

class AccueilViewTests(TestCase):
    def setUp(self):
        print("\n=== Début des tests de la page d'accueil ===")
        #Simulation test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author = Author.objects.create(
            author='Test Author',
            year_born=1980
        )
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            company_name='Test Company',
            address='Test Address',
            city='Test City',
            state='TS',
            zip_code='12345',
            telephone='123456789',
            fax='987654321',
            comments='Test Comments'
        )
        self.book = Title.objects.create(
            title='Test Book',
            year_published=2023,
            isbn='1234567890',
            pubid=self.publisher,
            description='Test Description',
            notes='Test Notes',
            subject='Test Subject',
            comments='Test Comments',
            genre='AUTRE'
        )
        
        # Créer un client et connecter l'utilisateur
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_accueil_view_status(self):
        print("\nTest 1: Vérification de l'accès à la page sans authentification")
        self.client.logout()  # On s'assure d'être déconnecté
        response = self.client.get(reverse('accueil'))
        print(f"-> Status code reçu: {response.status_code}")
        self.assertEqual(response.status_code, 200)  # Doit être accessible sans login

    def test_accueil_template_used(self):
        print("\nTest 2: Vérification du template utilisé")
        response = self.client.get(reverse('accueil'))
        print(f"-> Template utilisé: {response.templates[0].name}")
        self.assertTemplateUsed(response, 'registration/accueil.html')

    def test_accueil_context_data(self):
        print("\nTest 3: Vérification des compteurs dans le contexte")
        response = self.client.get(reverse('accueil'))
        print(f"-> Nombre d'auteurs: {response.context['author_count']}")
        print(f"-> Nombre d'éditeurs: {response.context['publisher_count']}")
        print(f"-> Nombre de livres: {response.context['book_count']}")
        self.assertEqual(response.context['author_count'], 1)
        self.assertEqual(response.context['publisher_count'], 1)
        self.assertEqual(response.context['book_count'], 1)

    def test_accueil_content(self):
        print("\nTest 4: Vérification des éléments HTML")
        response = self.client.get(reverse('accueil'))
        content = response.content.decode()
        
        # Vérifier la présence des éléments principaux
        elements = [
            'Votre super bibliothèque',
            'particles-js',
            'fa-users',
            'fa-building',
            'fa-book-open'
        ]
        for element in elements:
            print(f"-> Recherche de l'élément: {element}")
            self.assertIn(element, content)

    def test_accueil_counters_zero(self):
        print("\nTest 5: Vérification des compteurs à zéro quand il n'y a pas de données")
        # Supprimer toutes les données
        Title.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        print("-> Toutes les données ont été supprimées")

        response = self.client.get(reverse('accueil'))
        print(f"-> Nouveaux compteurs: Authors={response.context['author_count']}, Publishers={response.context['publisher_count']}, Books={response.context['book_count']}")
        self.assertEqual(response.context['author_count'], 0)
        self.assertEqual(response.context['publisher_count'], 0)
        self.assertEqual(response.context['book_count'], 0)

    def tearDown(self):
        print("\n=== Fin des tests de la page d'accueil ===")
