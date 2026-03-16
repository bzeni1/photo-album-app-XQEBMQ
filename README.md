# photo-album-PaaS


## 1. Projekt bemutatása

Django alapú webalkalmazás. 
Az alkalmazás hitelesített felhasználói rendszerrel működik, a képek Supabase Storage-ben tárolódnak, az adatbázis pedig Supabase PostgreSQL.

Az alkalmazás Docker konténerben fut, lokálisan Docker Compose segítségével indítható, éles környezetben pedig Render platformon kerül deployolásra.  

A projekt GitHub repositoryval van verziókezelve, és a Render automatikus deploy funkciója minden új commit esetén új buildet indít.

---

# 2. Választott környezet

Az alkalmazás egy **PaaS** környezetben fut.

A futtatási környezet a **Render platform**, amely biztosítja:

- a Docker konténer futtatását
- az alkalmazás internetes elérhetőségét
- a környezeti változók kezelését
- az automatikus build és deploy folyamatot

Az adatbázis és a fájltárolás egy külső managed szolgáltatásban, a **Supabase platformon** található.

---

# 3. Rendszer rétegei

Az alkalmazás több rétegből álló architektúrát követ.

### 1. Kliens réteg

A felhasználók böngészőn keresztül érik el az alkalmazást.  
A frontend megjelenítést a Django template rendszer biztosítja.

Feladata:

- felhasználói felület megjelenítése
- HTTP kérések küldése a szerver felé
- session cookie kezelése

---

### 2. Alkalmazás réteg

Az alkalmazás logikáját a Django backend valósítja meg.

Feladata:

- felhasználói autentikáció
- képek kezelésének logikája
- adatbázis műveletek
- fájlfeltöltések kezelése
- weboldalak generálása

A Django alkalmazás **Gunicorn WSGI szerveren keresztül fut** a Docker konténerben.

---

### 3. Adat réteg

Az adat réteg két részből áll.

**Supabase PostgreSQL**

- felhasználói adatok
- képek metaadatai
- Django session információk

**Supabase Storage**

- feltöltött képfájlok
- objektumtárolás felhőben
- publikus URL-ek generálása

---

# 4. Komponensek közötti kapcsolatok

A rendszer komponensei HTTP és adatbázis kapcsolatokon keresztül kommunikálnak.


A folyamat működése:

1. A felhasználó HTTP kérést küld a Django alkalmazás felé
2. A Django feldolgozza a kérést
3. Adatbázis műveletet hajt végre a Supabase PostgreSQL adatbázison (ha szükséges)
4. A feltöltött képek Supabase Storage-ben kerülnek tárolásra
5. A Django HTML oldalt generál és visszaküldi a böngészőnek

---

# 5. Használt technológiák

Backend: Django + Gunicorn  
Adatbázis: PostgreSQL (Supabase)  
Fájltárolás: Supabase Storage  
Konténerizáció: Docker  
Lokális fejlesztés: Docker Compose  
Deploy: Render (PaaS)  
Verziókezelés: Git + GitHub

---

# 6. Konténerizáció

Az alkalmazás Docker konténerben fut.

A Dockerfile definiálja az alkalmazás futtatási környezetét, a Docker Compose pedig a lokális fejlesztést segíti.

---

# 7. Fő funkciók

- felhasználói regisztráció
- bejelentkezés és kijelentkezés
- képfeltöltés
- képek listázása
- képek rendezése név vagy feltöltési dátum szerint
- hitelesített felhasználói hozzáférés
- automatikus build GitHub push esetén

---

# 8. Deploy folyamat

A deploy folyamat automatizált.

1. fejlesztő commitot készít
2. kód feltöltése GitHubra
3. Render érzékeli a változást
4. új Docker build indul
5. az alkalmazás új verziója deployra kerül

---

# 9. Projekt struktúra

```
/
├── album/
├── config/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

