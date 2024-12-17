from django.contrib import admin
from backoffice.models import Author, Publisher, Title, ReservationHistory
from django.utils.html import format_html

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(ReservationHistory)

class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_published', 'isbn', 'pubid', 'reserve_by', 'description', 'notes', 'subject', 'comments', 'image_preview')

    def image_preview(self, obj):
        if (obj.image):
            return format_html('<img src="{}" style="width: 50px; height: auto" />', obj.image.url)
        return 'Pas d\'image'
    image_preview.short_description = "Aperçu de l'image"

admin.site.register(Title, TitleAdmin)

