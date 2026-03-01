# photo-album-app-XQEBMQ

## 1. Projekt bemutatása

Django alapú webalkalmazás. 
Az alkalmazás hitelesített felhasználói rendszerrel működik, a képek Supabase Storage-ben tárolódnak, az adatbázis pedig Supabase PostgreSQL.

Az alkalmazás Docker konténerben fut, lokálisan Docker Compose segítségével indítható, éles környezetben pedig Render platformon kerül deployolásra.  
A GitHub repóhoz automatikus build és deploy van konfigurálva.


## 2. Használt technológiák

Backend: Django + Gunicorn  
Adatbázis: PostgreSQL (Supabase)  
Tárhely: Supabase Storage  
Konténer: Docker  
Lokális futtatás: Docker Compose  
Deploy: Render (Auto-Deploy)

## 3. Fő funkciók

- Felhasználói bejelentkezés, kijelentkezés, regisztráció
- Képfeltöltés
- Képek listázása
- Rendezés név vagy feltöltési dátum szerint
- Automatikus build GitHub push esetén

## Deploy

- Docker alapú szolgáltatás Renderen
- main branch
- Auto-Deploy bekapcsolva
- Környezeti változók külön beállítva

Minden GitHub push automatikusan új buildet indít.

## Projekt struktúra

/
├── album/
├── config/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
