from django.contrib import admin
from .models import Prijava, User, Smjer, Predmet


@admin.action(description='Upiši studenta')
def upis_studenta(modeladmin, request, queryset):
    queryset.update(status_prijave='+', profesor=request.user.ime + request.user.prezime)


@admin.action(description='Odbij prijavu studenta')
def odbijena_prijava(modeladmin, request, queryset):
    queryset.update(status_prijave='-', profesor=request.user.ime + request.user.prezime)


class PrijavaAdmin(admin.ModelAdmin):
    list_display = ('ime', 'prezime', 'email', 'mjesto_ro', 'datum_ro', 'molba', 'dokument', 'smjer_',
                     'profesor', 'odluka_donešena', 'status_prijave')
    actions= [upis_studenta, odbijena_prijava]
    
    def ime(self, obj):
        return obj.user.ime

    def smjer_(self, obj):
        return obj.smjer.naziv

    def prezime(self, obj):
        return obj.user.prezime

    def email(self, obj):
        return obj.user.email

admin.site.disable_action('delete_selected')
admin.site.register(Prijava, PrijavaAdmin)
admin.site.register(Smjer)
admin.site.register(User)
admin.site.register(Predmet)