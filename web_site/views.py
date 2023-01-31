from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm, PrijavaForm, NewAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Prijava, Smjer, Predmet


@login_required
def index(request):
    current_user = request.user.id
    prijave = Prijava.objects.filter(user=current_user)
    smjerovi = Smjer.objects.all()
    title = 'test'
    context = { 'title': title, 'prijave': prijave, 'smjerovi': smjerovi}
    #miće link za izradu prijave ukoliko je jedna od korisnikovih prijava prihvaćena
    for x in prijave:
        if x.status_prijave == '+':
            accepted = True
            context['accepted'] = accepted
            break
    return render(request, 'web_site/index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('web_site:index')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('web_site:index')
    form = NewUserForm()
    context = {'register_form':form}
    return render(request, 'web_site/register.html', context)


@login_required
def apply_request(request):
    if request.method == "POST":
        form = PrijavaForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('web_site:index')
    form = PrijavaForm(None)
    context = {'prijava_form':form}
    return render(request, 'web_site/apply.html', context)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('web_site:index')
    if request.method == "POST":
        form = NewAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('web_site:index')
    form = NewAuthenticationForm()
    context = {'login_form':form}
    return render(request, 'web_site/login.html', context)


def logout_request(request):
    logout(request)
    return redirect('web_site:index')


#dinamička izrada linkova za različite smjerove i njihove predmete
@login_required
def smjer(request, pk):
    smjer = Smjer.objects.filter(slug=pk)
    smjer_ = smjer[0].naziv
    smjer_id = smjer[0].id
    predmeti = Predmet.objects.filter(smjer=smjer_id)
    context = {'smjer': smjer_ , 'predmeti': predmeti}
    return render(request, 'web_site/smjer.html', context)