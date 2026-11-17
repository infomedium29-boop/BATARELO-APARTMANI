# Villa Batarelo — Evidencija izmjena 16.11.2026.

### Izvedeno
- Uklonjeni vizualni AI ukrasi (dekorativni brojevi, kružni pečat, strelice, apstraktna karta).
- Prirodniji tekstovi i lokalizacija HR / EN / DE.
- Jednostavniji sadržaji i kontakt; bez ponavljanja rezervacijskog bloka i naslova.
- Stvarna Google Maps karta koja se uključuje klikom; izleti s konkretnim poveznicama na kartu.
- Galerija više ne pokazuje pogrešne rezervne fotografije i ima poruku za nedostupne slike.
- Dovršeni sadržajni nacrti pravnih stranica (potvrda službenih podataka još je potrebna).
- Postojeći intro, lebdeća navigacija, jezici, upit i kontaktni gumbi sačuvani.

### Otvoreno prije javne objave
- Originalne fotografije i dopuštenja za korištenje. Postojeći vanjski URL-ovi nisu pouzdana trajna zamjena.
- Konačni podaci registriranog iznajmljivača te vlasnička potvrda pravnih tekstova.
- Potvrda kapaciteta, kućnog reda, ocjena i uvjeta rezervacije.
- Domena, opcionalna analitika / servis za e-mail upite prema dogovoru.

## Logo bez kućice — 16.11.2026.
- Uklonjen SVG simbol kućice iz navigacije i podnožja na svih 30 podstranica (HR, EN, DE).
- Logo je samo tipografski naziv „Villa Batarelo”, bez lokacijskog potpisa.
- Intro otkriva naziv elegantnom tekstualnom animacijom, bez simbola.
- Favicon zamijenjen čistom tipografskom verzijom s nazivom.
- Izmjene unesene i u generator `tools/build_site.py`, pa ostaju nakon ponovne izrade.
- Ostale sekcije i funkcije nisu mijenjane.

## Klikabilna stvarna karta — 16.11.2026.
- Na lokaciji HR/EN/DE odmah je prikazana prava Google Maps karta s označenom lokacijom Ville Batarelo.
- Klik na cijelu kartu vodi na Google Maps poslovni zapis Ville Batarelo.
- Uklonjen tekstualni okvir s gumbom; usklađeni pravni nacrti i trajni HTML generator.

## 16. 11. 2026. — Poravnanje datuma na mobitelima
- Ispravljena iOS Safari širina polja za datum dolaska i odlaska na obrascu rezervacija.
- Datumska polja sada koriste širinu istog stupca kao Broj gostiju i Ime i prezime.
- Nisu mijenjani podaci, obrazac, dizajn ostalih polja, kalendar ili funkcionalnosti.

- Intro sada koristi pozadinsku fotografiju stvarnog objekta uz zadržanu animaciju naziva.

## Optimizacija desktop intro animacije

- Na ekranima širim od 980 px pozadinska fotografija intra ostaje statična kako bi izbjegli skupo animiranje velikog sloja.
- Uklonjeno dinamičko zamućenje (`backdrop-filter`) s desktop intra, uz zadržan suptilan proziran okvir.
- Animacija naziva i završni prijelaz ostaju, uz kraće trajanje otkrivanja naziva.
- Mobilni intro, uključujući njegov izgled i animaciju, nije mijenjan.

- U introu je potpuno uklonjen blur efekt, a pozadinska fotografija je dodatno prigušena jačim overlayem.

- Intro: uklonjen sivi/tamni panel, obrub i sjena iza naziva na desktopu i mobitelu; naziv Villa Batarelo animira se izravno preko prigušene fotografije objekta.

## 16.11.2026. — Jezična i sadržajna dorada
- Zamijenjen gumb „Istražite vilu” prirodnijim „Pogledajte vilu” (EN: View the villa; DE: Villa ansehen).
- Pregledani sadržaji svih 30 HR/EN/DE HTML stranica: naslovi, opisi, CTA poveznice, sadržaji, lokacija, upit, FAQ i pravne stranice.
- Uklonjene generičke poruke i ponavljanje neodređenog „Saznajte više”; poveznice sada imenuju svoje odredište.
- Ujednačeni prirodni opisi sobe, terase, bazena, lokalnih izleta i kontakta; nisu dodavani novi nepotvrđeni sadržaji objekta.
- Pravni uvjeti nisu izmišljani ili proširivani; samo uvodne rečenice prilagođene svrsi stranice.
- Zadržani su prethodni premium intro bez sive pozadine/obruba, Google karta, mobilni navigacijski raspored i popravak datuma.
- Izvorni CSS, JavaScript i postojeći izvori fotografija ostali su nepromijenjeni.
- Provjereni su interni URL-ovi, broj H1 po stranici, sve jezične verzije i JavaScript sintaksa.
- Vizualno testiranje u pregledniku nije bilo moguće zbog blokade pokretanja lokalne stranice u testnom okruženju; provjeriti stvarni izgled nakon deploya.


## 16.11.2026. – iPhone/Safari polja datuma (drugi, robusniji ispravak)
- Polja dolaska i odlaska imaju isti točan vizualni okvir i širinu kao „Broj gostiju“ i „Ime i prezime“.
- iPhone Safari više ne iscrtava native datumski okvir izvan forme: pravi `type=date` ostao je kao prozirni interaktivni sloj unutar točno dimenzioniranog okvira.
- Izvorni kalendarski odabir i provjera datuma ostali su aktivni. Odabrani datum prikazuje se u skladu s HR/EN/DE jezikom.
- Promjene se odnose isključivo na polja datuma, povezani JavaScript i stilove rezervacijskog obrasca.

- Naslov „Telefon i e-mail” na stranici rezervacija prilagođen je mobilnim i tablet zaslonima tako da ne prelazi u drugi red; izmjena vrijedi i za EN/DE.
