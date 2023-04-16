#kütüphaneleri yükleme
import folium
import requests
from bs4 import BeautifulSoup as bs
from folium import plugins
import pandas

#kullanıcıdan bilgi alma
sayi = int(input('Kaç deprem listelensin (3-5-10-15): '))

#veri çekme
r = requests.get('http://www.koeri.boun.edu.tr/scripts/lst5.asp')
soup = bs(r.content, 'lxml')
info = soup.text.split('-------------')[2][:1900]

x = 1
y = 0
koordinatList = []
buyuklukList = []
tarihList = []
saatList = []
derinlikList = []
while y < sayi:
    tarihList.append(info[x:x+21].split()[0])
    saatList.append(info[x:x+21].split()[1])
    koordinatList.append(info[x+23:x+40])
    derinlikList.append(info[x+47:x+54])
    buyuklukList.append(info[x+62:x+65])
    x += 129
    y += 1

#folium kütüphanesini kullanarak veri işleme
m = folium.Map(location=[38.76534530779815, 35.44033727686726], zoom_start=6, min_zoom=6, tiles='OpenStreetMap')
minimap = plugins.MiniMap().add_to(m)

a = 0
while a < len(buyuklukList):
    x_koordinati = float(koordinatList[a].split()[0])
    y_koordinati = float(koordinatList[a].split()[1])
    bilgi = '''
    Tarih: {}     
    Saat: {}              
    Derinlik: {} km
    Büyüklük: {} ML
    '''.format(tarihList[a],saatList[a],derinlikList[a],buyuklukList[a])


    iframe = folium.IFrame(bilgi)
    popup = folium.Popup(iframe, min_width=150, max_width=250)
    folium.Circle(radius=int(float(buyuklukList[a])*10000),location=[x_koordinati,y_koordinati],color='crimson',fill_color='red', popup = popup).add_to(m)
    a += 1
    
#kayıt işlemi
m.save(f"son_{sayi}_deprem.html")
