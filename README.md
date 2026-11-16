# Villa Batarelo — Medium29

**Revizija: 16. studenoga 2026. · HR / EN / DE · GitHub + Cloudflare Pages**

## Što je izrađeno

Kompletan višestranični statički web (30 HTML stranica: po 10 za hrvatski, engleski i njemački, plus `/` preusmjeravanje). Projekt sadrži premium intro, lebdeću i mobilnu navigaciju, prikaz smještaja, galeriju s filtrima i lightboxom, lokaciju s Google Maps kartom, informacije o izletima, ocjene gostiju, neobvezujući upit za boravak i tri pravne podstranice na svakom jeziku.

### Izmjene ove revizije

- Uklonjeni su ukrasni brojevi, većina besmislenih strelica, kružni pečat na fotografiji i apstraktna topografska ilustracija.
- Zamijenjeni su generički naslovi prirodnim opisima smještaja na HR, EN i DE; pojednostavljen sadržaj izleta, kontakta i smještaja.
- Uklonjeni su duplicirani naslovi i izbjegnuta su stalna ponavljanja iste rezervacijske sekcije; ocjene su pomaknute bliže početku naslovnice.
- Svi ranije uočeni engleski natpisi zamijenjeni su prijevodima ili uklonjeni.
- Stvarna lokacija na karti: Google Maps iframe učitava se **isključivo nakon klika**. Alternativna poveznica otvara adresu u Google Kartama. Kartice za izlete imaju funkcionalne kartografske poveznice.
- Galerija ne zamjenjuje neuspjelo učitane fotografije pogrešnim kadrovima iste vile: umjesto ponavljanja takve se pločice skrivaju, a ako nema vidljivih fotografija prikazuju se poveznice na oglase.
- Prošireni su informativni tekstovi privatnosti, kolačića i pravila boravka, bez izmišljenih registracijskih podataka.
- Zadržani su premium intro, odobrena mobilna navigacija, jezični izbornik, WhatsApp i telefon, galerijski filteri, pregled fotografija i forma za upit.

## GitHub i Cloudflare Pages

1. Raspakirajte ZIP te **sadržaj** prenesite u GitHub repozitorij.
2. U Cloudflare Pages: `Connect to Git` → odaberite repozitorij.
3. `Framework preset: None`, `Build command: (prazno)`, `Build output directory: .` (točka).
4. Nakon deploya otvorite `/hr/`, `/en/`, `/de/`, `/sitemap.xml` i `robots.txt`.

Statičke HTML datoteke već su generirane; Python nije potreban na Cloudflareu. Cloudflare Pages Functions nalaze se u `/functions` te podešavaju apsolutni canonical i hreflang prema domeni deploya.

## Fotografije — VAŽNO

**Fotografije trenutačno nisu lokalno u ZIP-u.** U HTML-u je 35 jedinstvenih URL referenci na fotografije Ville Batarelo preko javno dostupnih izvora povezanih s oglasima. Njihova trajna dostupnost nije zajamčena, a svi se izvori nisu mogli provjeriti učitavanjem iz ovog okruženja. Neke slike možda neće biti vidljive ako udaljeni poslužitelji zabrane izravan prikaz.

- Popis izvora: `assets/img/photo-manifest.json`.
- Postojeći prikazi koristili su i nekoliko javnih fotografija istog objekta s `static.cupid.travel`.
- Ako URL ne uspije, pločica se ne zamjenjuje kadrom iz pogrešne prostorije. U drugim sekcijama koristi se zamjenski vizual kao posljednja opcija.
- Zatražiti izvorne fotografije od Davora te potvrdu prava na njihovu objavu. Tek tada fotografije lokalno optimizirati i zamijeniti URL-ove.
- Opcionalni alat za računalo s mrežnim pristupom: `tools/download_photos.py` (samo nakon odobrenja vlasnika, bez zaobilaženja zaštite). Za lokalni uvoz potrebno je instalirati `requests`, `pillow`, `pillow-avif-plugin`, `jinja2`, zatim pokrenuti alat i `python3 tools/build_site.py`.
- Za produkciju je preporučljivo lokalno poslužiti AVIF/WebP varijante, a ne oslanjati se trajno na Bookingove vanjske URL-ove.

## Obrazac i kontakt

Rezervacijski obrazac provjerava datume, broj gostiju, podatke i privolu te priprema poruku za WhatsApp ili program za e-mail. **Ne potvrđuje rezervaciju, ne sprema podatke na poslužitelj i ne šalje poruku automatski.** Posjetitelj je sam mora poslati u otvorenoj aplikaciji.

Telefon, e-mail i WhatsApp podešavaju se u `assets/js/config.js` i sadržaju generatora `tools/build_site.py`. Automatsko slanje Web3Forms putem backend servisa nije povezano.

## Pravni tekstovi i podatci — za potvrdu prije objave

Pravne podstranice sada imaju smislen informativni sadržaj i ne prikazuju radne napomene gostima, ali **nisu odobreni konačni pravni tekstovi**. Prije javne objave vlasnik ili pravni stručnjak treba potvrditi:

1. Pun službeni naziv i podatke registriranog pružatelja smještaja / voditelja obrade, adresu i kontakt.
2. Točne uvjete smještaja, avanse, otkazivanja, check-in/check-out, mogućnost boravka kućnih ljubimaca, kapacitet i broj kupaonica.
3. Izjavu o privatnosti uključujući pravni temelj, rokove čuvanja podataka i primatelje, ovisno o stvarnom procesu zaprimanja rezervacija.
4. Objavljivanje fotografija i stvarne Booking/Airbnb ocjene.
5. Povezivanje vlastite domene i eventualne analitike. GA4 je zadano isključen dok se u `assets/js/config.js` ne doda ID; opcionalno učitavanje poštuje privolu.

## Održavanje

Glavni izvor za tekstove i HTML predloške: `tools/build_site.py`. Nakon uređivanja pokrenuti:

```bash
python3 -m pip install jinja2
python3 tools/build_site.py
```

Za stilove `assets/css/site.css`, za interakcije `assets/js/site.js`. Sve generirane HTML datoteke već su u ZIP-u.

*Izradio Medium29, studeni 2026.*
