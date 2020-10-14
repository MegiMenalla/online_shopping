from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import *

# Create your views here.


def home(request):
    dyqane = Dyqan.objects.all()
    produkte = Produkt.objects.all()

    data = {
        'dyqane': dyqane,
        'produkte': produkte,

    }
    return render(request, 'homepage.html', data)


def dyqan(request, pk):
    dyqan = Dyqan.objects.get(id=pk)
    produktet = DyqanProdukt.objects.filter(dyqan=dyqan)

    data = {
        'dyqan': dyqan,
        'produktet': produktet,
    }
    return render(request, 'dyqan.html', data)


def prod_dyqan(request, pk):
    dyqanprodukt = DyqanProdukt.objects.get(id=pk)
    produkt = Produkt.objects.get(id=dyqanprodukt.produkt.id)
    dyqanet = DyqanProdukt.objects.filter(produkt=produkt).order_by('cmimi')
    data = {
        'dyqanprodukt': dyqanprodukt,
        'produkt': produkt,
        'dyqanet': dyqanet,

    }
    return render(request, 'produkt.html', data)


def inventar(request, pk):
    dyqan = Dyqan.objects.get(id=pk)
    emer = dyqan.emer
    produktet = DyqanProdukt.objects.filter(dyqan=dyqan)

    total_produkt = 0
    for i in produktet:
        total_produkt += i.cmimi * i.sasia

    tipe = set()
    for i in produktet:
        tipe.add(i.produkt.tip)

    dict_tipe = {}

    for j in tipe:
        total_per_tip = 0
        for i in produktet:
            if i.produkt.tip == j:
                total_per_tip += i.cmimi * i.sasia
        dict_tipe.update({j: total_per_tip})

    data = {
        'dyqan': dyqan,
        'total_produkt': total_produkt,
        'emer': emer,
        'vlera_per_tipe': dict_tipe,
    }
    return render(request, 'inventar.html', data)


def kategori(request, pk):
    data = {}
    return render(request, 'kategori.html', data)


@login_required(login_url='logini')
def porosite_e_mia(request):
    user = request.user
    porosite = user.profil.porosite.all()

    # print(porosite)
    data = {
        'porosite': list(porosite),
    }
    return render(request, 'klient.html', data)


@login_required(login_url='logini')
def bli(request, pk):
    user = request.user
    porosia = DyqanProdukt.objects.get(id=pk)
    emer1 = porosia.produkt.emer
    emer2 = porosia.dyqan.emer
    form_shto = BliForm(instance=porosia)
    if request.method == 'POST':
        form = BliForm(request.POST, instance=porosia, )
        if form.is_valid():
            if porosia in request.user.profil.porosite.all():
                return HttpResponse(
                    'Ju e kemi rezervuar nje here kete produkt. Paguani dhe  rifutuni per te blere perseri.')

            if int(porosia.sasia) > 0:
                porosia.dekremento()
                porosia.save()
                user.profil.porosite.add(porosia)
                user.save()
                return redirect('porosite_e_mia')
            else:
                return HttpResponse('Ky produkt ka mbaruar. Mund te kerkoni ne dyqane te tjera ose '
                                    'te provoni perseri me vone.')

    data = {

        'form_shto': form_shto,
        'emer1': emer1,
        'emer2': emer2,

    }
    return render(request, 'shto_ne_karte.html', data)


@login_required(login_url='logini')
def hiq(request, pk):
    user = request.user
    porosia = DyqanProdukt.objects.get(id=pk)

    porosia.inkremento()
    porosia.save()

    user.profil.porosite.remove(porosia)
    user.save()

    porosite = user.profil.porosite.all()

    data = {
        'porosite': porosite,

    }
    return render(request, 'klient.html', data)


@login_required(login_url='logini')
def paguaj(request):
    user = request.user

    user.profil.porosite.clear()
    user.save()

    return render(request, 'pagesa.html')


@unauthenticated_user
def regjistrohu(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Profil.objects.create(
                user=user,
            )
            messages.success(request, 'Profili u kijua.')
            return redirect('logini')

    data = {
        'form': form,

    }
    return render(request, 'registration/regjistrohu.html', data)


@unauthenticated_user
def logini(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Emri ose kodi eshte gabim!')
            return render(request, 'registration/login.html', data)
    else:
        return render(request, 'registration/login.html', data)


def logoutUser(request):
    logout(request)
    return redirect('logini')
