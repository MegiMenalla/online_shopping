# 0 tip_produkti,#1 id_produkti #2 emerProdukti, #3 img_scr, #4 pershkrim, #5 id_dyqani, #6 emerDyqani, #7 adresa,
# #8 logo, #9 cmimi, #10 sasia
import csv
from shops.models import Produkt, Dyqan, DyqanProdukt


def krijo_produkt(id, tip, emer, img, pershk):
    produkt = Produkt(
        id=id,
        tip=tip,
        emer=emer,
        img_src=img,
        pershkrim=pershk
    )
    produkt.save()


def krijo_dyqan(id, emer, adresa, logo):
    dyqan = Dyqan(
        id=id,
        emer=emer,
        adresa=adresa,
        logo=logo,
    )
    dyqan.save()


def krijo_DyqanProdukt(id_prod, id_dyqan, cmimi, sasia):
    dp = DyqanProdukt(
        produkt=id_prod,
        dyqan=id_dyqan,
        cmimi=cmimi,
        sasia=sasia
    )
    dp.save()


def krijo_lidhje(id_produkt, id_dyqan, cmimi, sasia):
    produkti = Produkt.objects.get(id=id_produkt)
    dyqani = Dyqan.objects.get(id=id_dyqan)
    dyqani.produkte.add(produkti, through_defaults={'cmimi': cmimi, 'sasia': sasia})
    dyqani.save()


def krijo_produktet():
    with open('dyqane.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for line in reader:
            id = line[1]
            tip = line[0]
            emer = line[2]
            img_src = line[3]
            pershkrim = line[4]

            krijo_produkt(id, tip, emer, img_src, pershkrim)


def krijo_dyqanet():
    dyqane = []
    with open('dyqane.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for line in reader:
            dyqani = line[5]
            if dyqani not in dyqane:
                dyqane.append(dyqani)
                emer = line[6]
                adresa = line[7]
                logo = line[8]
                krijo_dyqan(dyqani, emer, adresa, logo)


def krijo_lidhjet():
    with open('dyqane.csv', 'r', encoding='utf8') as data:
        reader = csv.reader(data)
        for line in reader:
            id_produkti = line[1]
            id_dyqani = line[5]
            cmimi = line[9]
            sasia = line[10]
            krijo_lidhje(id_produkti, id_dyqani, cmimi, sasia)



def zbraz():
    Produkt.objects.all().delete()
    Dyqan.objects.all().delete()
    DyqanProdukt.objects.all().delete()


def PodukteCounter():
    return Produkt.objects.all().count()


def DyqaneCounter():
    return Dyqan.objects.all().count()


def run():
    print('Pastrim i DB ...')
    zbraz()
    print('Numri i produkteve para ...', PodukteCounter())
    print('Krijo produkte ...')
    krijo_produktet()
    print('Numri i produkteve pass...', PodukteCounter())
    print('Numri i dyaneve para ...', DyqaneCounter())
    print('Krijo dyqane ...')
    krijo_dyqanet()
    print('Numri i dyqaneve pas ...', DyqaneCounter())
    print('krijo lidhjet')
    krijo_lidhjet()

