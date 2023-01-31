from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from django.contrib.auth.models import UserManager, PermissionsMixin


#novi superuser
class UserManager(BaseUserManager):
    def create_superuser(self, ime, prezime, email, password=None):

            user = self.model(
                email=self.normalize_email(email)
            )
            user.ime = ime
            user.prezime = prezime
            user.set_password(password)
            user.is_admin = True
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.save(using=self._db)
            return user


#novi user
class User(AbstractBaseUser, PermissionsMixin):
    ime = models.CharField(max_length=20, null=True)
    prezime = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ime', 'prezime']

    objects = UserManager()

STATUS_CHOICES = [
    ('n', 'Neodređen'),
    ('+', 'Odobren'),
    ('-', 'Odbijen'),
]

#smjerovi
class Smjer(models.Model):
    naziv = models.CharField(max_length=20, null=False)
    kvota = models.IntegerField()
    #slug za dinamičke web stranice
    slug = models.SlugField(default='', blank=True, null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.naziv)
        super().save(*args, **kwargs)
    

#prijave
class Prijava(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    datum_ro = models.DateField(null=True)
    mjesto_ro = models.CharField(max_length=20, null=True)
    molba = models.TextField(max_length=200, null=True, unique=True)
    dokument = models.FileField(upload_to='uploads/', null=True)
    prosjek = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00), MinValueValidator(2.00)])
    ocjena_matura = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00), MinValueValidator(2.00)])
    status_prijave = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    profesor = models.CharField(max_length=20, blank=True)
    odluka_donešena = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True)
    smjer = models.ForeignKey(Smjer, on_delete=models.CASCADE, null=True)
    

#predmeti
class Predmet(models.Model):
    ime_predmeta = models.CharField(max_length=30, null=True)
    ects = models.IntegerField(validators=[MaxValueValidator(9), MinValueValidator(2)])
    smjer = models.ForeignKey(Smjer, on_delete=models.CASCADE, null=True)