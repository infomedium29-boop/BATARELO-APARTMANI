# Villa Batarelo — statička višestranična web stranica

**Status: gotov funkcionalni prototip za pregled, nije odobren za javnu objavu bez potvrde vlasnika.**

## Sadržaj

- 30 stvarnih HTML podstranica (10 × HR, EN, DE) + preusmjeravanje s početne `/` na `/hr/`.
- Premium intro (jednom po sesiji), lebdeća navigacija, fotografije vile, filter galerija, lightbox, FAQ, višejezični SEO sadržaj.
- Obrazac za neobvezujući upit: validira datume i podatke te priprema **WhatsApp poruku**. Sekundarno otvara unaprijed popunjen e-mail. Nema automatskog slanja e-maila s poslužitelja, automatske rezervacije ili plaćanja.
- Cookie izbor se sprema lokalno. GA4 je isključen dok se ID ne unese u `assets/js/config.js`; opcionalna analitika učitava se tek uz privolu.
- Dinamički `sitemap.xml` i `robots.txt` preko Cloudflare Pages Functions, s pravom domenom deploya.

## Deploy na GitHub i Cloudflare Pages

1. Raspakirajte ZIP i prenesite **sadržaj mape** u novi GitHub repozitorij (ili upload ZIP raspakiranog sadržaja).
2. Cloudflare → Workers & Pages → Create → Pages → Connect to Git → odaberite repozitorij.
3. **Framework preset: None**. **Build command: prazno**, **Build output directory: `/`** (repozitorij je gotova statička web stranica).
4. Objavite i otvorite `/hr/`, `/en/`, `/de/` i `/sitemap.xml`.
5. Ako Cloudflare UI ne prihvaća `/` za output, upišite `.` (točka).

## VAŽNO: fotografije

Izravno preuzimanje originala s Bookinga i Airbnba nije bilo dostupno u radnom okruženju. Stoga **fotografije trenutačno nisu spremljene lokalno niti konvertirane u AVIF**. Povezane su kao vanjski resursi koji mogu prestati raditi zbog promjene URL-a ili hotlink zaštita.

- 4 visoko-rezolucijske fotografije stvarne Ville Batarelo imaju verificirane javne URL-ove na povezanom izvoru.
- Dodatne fotografije su navedene kroz Booking CDN prema javno indeksiranoj galeriji; nisu potvrđeni svi URL-ovi visoke razlučivosti. Kod neuspjelog učitavanja prikazuje se verificirana fotografija **istog objekta**, ne druge vile.
- Popis: `assets/img/photo-manifest.json`.
- Kad Davor dostavi izvorne fotografije i potvrdi pravo njihove uporabe, treba ih staviti u `assets/img/`, optimizirati u AVIF s fallbackom, te zamijeniti URL-ove u `tools/build_site.py`, pa ponovno pokrenuti `python tools/build_site.py`.
- Ne objavljivati fotografije za koje vlasnik nema odgovarajuća prava.

## Upute prije javne objave

1. Potvrditi kapacitet (Airbnb navodi 6 gostiju u rezervacijskom pregledu, opis 6+1), broj kreveta/kupaonica, stvarne sadržaje, uvjete dolaska i odlaska.
2. Potvrditi e-mail, broj telefona i registrirane podatke davatelja usluge. U tekstu postoje kontaktni podaci dostavljeni u Meta obrascu.
3. Provjeriti i odobriti pravne tekstove — trenutno su nacrti, a ne konačni pravni savjet.
4. Ponovno provjeriti Booking i Airbnb ocjene: 10/10 i 4,96/5 bile su vidljive u trenutku istraživanja.
5. Fotografije lokalizirati i optimizirati u AVIF nakon što ih Davor pošalje.
6. Potvrditi domenu. Cloudflare Pages middleware u `functions/_middleware.js` automatski dodaje apsolutni canonical i hreflang za domenu na kojoj je otvoren sajt. Ako sajt koristite na hostingu bez Cloudflare Pages Functions, te tagove treba generirati pri buildu.
7. GA4, Web3Forms ili kalendar rezervacija **nisu povezani**. Obrazac radi putem WhatsApp/mailto komunikacije.
8. Ako se zamijene svi podaci i potvrde pravne stranice, izbaciti obavijesti o radnoj galeriji i pravnom nacrtu iz sadržaja prije objave.

## Izmjena sadržaja

Izvor za izgradnju svih stranica: `tools/build_site.py`. Nakon promjena pokrenite:

```bash
python3 tools/build_site.py
```

Na Cloudflare Pages se učitavaju već generirane HTML datoteke, nema potrebe za Python buildom na Cloudflareu.

**Izradio Medium29 — studeni 2026.**

## Opcionalni automatski uvoz fotografija na računalu s internetom

Ako Davor potvrdi prava na objavu postojećih fotografija, možete pokušati lokalizirati javno dostupne slike bez zaobilaženja zaštita:

```bash
python3 -m pip install requests pillow pillow-avif-plugin jinja2
python3 tools/download_photos.py
python3 tools/build_site.py
```

Skripta sprema preuzete fotografije u `assets/img/villa/` (AVIF + WebP fallback), zapisuje dostupnost u `photo-map.json` i preskače nedostupne, presitne ili blokirane izvore. **Nije pokretana u ovom okruženju jer nema pristupa preuzimanju datoteka s tih domena.** Ne jamči da će platforme dopustiti preuzimanje niti da su sve fotografije dostupne.
