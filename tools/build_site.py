from pathlib import Path
from html import escape
import json
from jinja2 import Environment, BaseLoader
ROOT=Path(__file__).resolve().parents[1]
BOOKING='https://www.booking.com/hotel/hr/villa-batarelo-sinj.html'
AIRBNB='https://hr.airbnb.com/rooms/11475202'
WA='385955846044'
# Independently verified photos of this actual property from indexed pages.
CUPID='https://static.cupid.travel/hotels/'
FALLBACKS=[CUPID+'566979439.jpg',CUPID+'507662904.jpg',CUPID+'507662891.jpg',CUPID+'507662909.jpg']
# Additional actual property images indexed through the Booking-powered gallery.
# URLs use Booking CDN. These remain remote references until the owner supplies original files.
RAW=[
('566981809','ee2a5e0adad52d45d961566a248429c582057ec2e1b8f77fed4607f1a9aa8999','exterior'),
('566980468','8bd7bcf3751bf0165c4d70b1052afd142e157a492865fe167011ae8685ef8e35','pool'),
('507662613','462a63928f0fdf930cf583ca5279455f4ebf3bb5a4ef5e203ec40d8c13c68d38','pool'),
('507662656','0189e98720f1ea0d4d86f5fb81c385237f8aec3d04f71da36d150612b524a025','outside'),
('566981788','9d48aad0dd669dd30a679fa16f27917b96f210c568bc8ddcb7bb90043bf6c2c0','pool'),
('507662764','137fc5ef3c682fd24ca94e2f6ca0d85c111bf207d295f4de6d5ba077e572ad91','pool'),
('507662686','ea9f244612e1fa12b732e6171876628a39182b5f43be98704a96b48c2b771ea1','pool'),
('507662674','f090adf0c46fad5fc8732949eec9b66f5600e240b060a4b1e79de70a04cd6e15','pool'),
('507662721','5b1deba7844228d5ee9e369b6dc1774a1207b2e49433a6289dbabeee3716ebf2','pool'),
('507662743','88e375bbfd73722a73e5cd5a93008144864e342fac587b0173e08f4d9892e26b','pool'),
('507662912','eb74af00d8e2ecc5c9f22a4e19d6e38fe2295b0e3ff9c0d8151e8dc93caf13ce','pool'),
('507662869','769211ab987aeb9b62f1b36950de6534e26049f0ab554bc7c3251557fe8b0472','outside'),
('507662607','ae200dbb72dca433e4e56dea53b9b843f19fe72eefa526a165528d9423205a90','inside'),
('507662778','405bdebae680ce0ea5c86a4ab322b5b00e2b11cd67c0f9f89cfa7b63b6429932','inside'),
('507662697','8f16d07e9ace003b2625a5f12aa0be7b6db137c215191fd6228292ee9dd7050e','inside'),
('507662738','23095f32de5891b7049a2a065e5612548d2150a5dfc197e597df5b504475b6e3','inside'),
('507662770','1d82c363aa393096ecaadf5b990dd91d6632e1fbff12457af0d1745857dd8c76','inside'),
('507662796','fba388ba399ad91b5af3660c82d3f3885c88abc8c8d49b147e7c7d0379e99c13','inside'),
('507662774','b7745eca4583a00685ce7c52dfbe4aa72170f5b8245fdd88f7fb91481e9b71f9','inside'),
('507662862','60d15d736c81f69b5d9ef4e758423f74a0007b95a1855a2dcd89dcc213cbb365','inside'),
('566977587','fe457fbd9ed2c9b4a213137852e2d67b4d5baee6973b658901b44b3faa165829','inside'),
('507662651','0705e3c9b56dc1ceb7e08729d29d81d3d6951752cc88ccf63744c92aa409ad47','bedroom'),
('566977569','b9077263d4a6e90f1494e306e5427e46be158a5ff756da9feae155f6f786c79d','bedroom'),
('566977585','f2e4d375dcc7956ef02b3c38c5cbd2c16243015e7a05df8e53fdeab07147e63c','bedroom'),
('566977582','9d210ed8360999e344559785ba52a3c3acfb39db5092d5fdba661226748cc8ae','bedroom'),
('507662790','a2b332f6ecd76d7701f9cb7d99691650aa4ac75768759c23305fd16cf405c561','bedroom'),
('507662727','c216e6574af1f31762be67677dc88ba76d57910db2ff3499e25deac8ad3bf726','bathroom'),
('566977871','45dc1a1331cb3a14fbadce519eaf84353cb93269dfb0244b3f80389be77c7d91','bedroom'),
('507662631','15f0a7e04863ab2e35886ae52933f6494fcfd0b3d3714aaf7d111376dae19631','outside'),
('507662668','a539be0a4b88732234f45f4fb9d49f12515ea4c6d80958c113e9955a43efd94e','inside'),
('507662747','2bf340a2b83d76b2c9ff39a6e1d6b06915672cc1052e35fa6d0ade0d46904e9e','outside'),
]
# Actual verified high-resolution images are prioritized for editorial usage.
photos=[{'src':FALLBACKS[0], 'fallback':FALLBACKS[0], 'category':'exterior','id':'cover','hero':True},
        {'src':FALLBACKS[1], 'fallback':FALLBACKS[1], 'category':'outside','id':'terrace'},
        {'src':FALLBACKS[3], 'fallback':FALLBACKS[3], 'category':'bedroom','id':'bedroom-main'},
        {'src':FALLBACKS[2], 'fallback':FALLBACKS[2], 'category':'pool','id':'pool-evening'}]
for pid,key,cat in RAW:
    photos.append({'src':f'https://cf.bstatic.com/xdata/images/hotel/max1024x768/{pid}.jpg?k={key}&o=',
                   'fallback':FALLBACKS[{'exterior':0,'pool':2,'outside':1,'bedroom':3}[cat]] if cat in ['exterior','pool','outside','bedroom'] else '/assets/img/photo-pending.svg', 'id':pid,'category':cat})
# Replace remote URLs with downloaded images when owner-approved local copies exist.
_original_photos = [p.copy() for p in photos]
_local_map_path = ROOT / 'assets' / 'img' / 'photo-map.json'
if _local_map_path.exists():
    local_map = json.loads(_local_map_path.read_text(encoding='utf8'))
    for photo in photos:
        if photo['id'] in local_map:
            image_paths = local_map[photo['id']]
            if (ROOT / image_paths['src'].lstrip('/')).is_file():
                photo['src'] = image_paths['src']
                photo['fallback'] = image_paths['fallback']
LANGS={
'hr':{
'locale':'hr_HR','tagline':'Privatna vila s bazenom · Lučane kod Sinja',
'nav':{'home':'Početna','villa':'O vili','amenities':'Smještaj','gallery':'Galerija','location':'Lokacija','booking':'Dostupnost','contact':'Kontakt','privacy':'Privatnost','cookies':'Kolačići','terms':'Uvjeti boravka'},
'cta':'Pošaljite upit','explore':'Istražite vilu','check':'Provjerite dostupnost','view_gallery':'Pogledajte galeriju','learn':'Saznajte više','see_all':'Sve fotografije','view_details':'Detalji smještaja',
'home_title':'Vaš prostor za <em>pravi odmor.</em>','home_sub':'Privatni bazen, prostrana okućnica i mir Lučana, svega nekoliko kilometara od Sinja. Cijela vila samo za vas.',
'eyebrow':'VILLA BATARELO · SINJ, HRVATSKA','stats':['3 spavaće sobe','Privatni bazen','Cijela vila','Besplatan parking'],
'home_intro_k':'MIR KOJI IMA SVOJE MJESTO','home_intro_title':'Dani bez žurbe. <em>Prostor samo za vas.</em>','home_intro_text':'U Lučanima, nedaleko od Sinja, Villa Batarelo pruža privatnost koju je teško pronaći u užurbanim ljetnim odredištima. Dan započinje uz bazen, nastavlja se dugim ručkom na terasi, a završava pod otvorenim nebom.',
'photo_pool_k':'ŽIVOT NA OTVORENOM','photo_pool_t':'Bazen, terasa i <em>vrijeme zajedno.</em>','photo_pool_p':'Provedite dan uz vodu, pripremite roštilj ili uživajte u večeri na natkrivenoj terasi. Vanjski prostor pripada isključivo vašoj grupi.',
'main_amen_k':'UDOBNOST ZA CIJELU EKIPU','main_amen_t':'Sve što vam je potrebno, <em>na jednom mjestu.</em>',
'amen_short':['Tri odvojene spavaće sobe za miran san.','Klimatizirani interijer, potpuno opremljena kuhinja i dnevni prostor.','Vlastiti bazen, terasa, roštilj i uređena okućnica.'],
'gallery_k':'MALI POGLED U NAŠ SVIJET','gallery_t':'Prostor koji <em>priča fotografijama.</em>',
'location_k':'DALMATINSKO ZALEĐE','location_t':'Dovoljno blizu svemu. <em>Dovoljno daleko od gužve.</em>','location_p':'Villa Batarelo nalazi se u Lučanima, približno 3,5 km od Sinja. Ovdje možete uživati u miru prirode, a pritom lako istraživati kulturne znamenitosti, Cetinu i dalmatinsku obalu.',
'reviews_k':'DOJMOVI GOSTIJU','reviews_t':'Lijepo je kada se gosti <em>rado vraćaju.</em>','review_info':'Ocjene prema javnim oglasima; mogu se promijeniti. Kliknite za aktualne recenzije.',
'booking_banner_k':'PLANIRATE ODMOR?','booking_banner_t':'Vaš sljedeći odmor <em>počinje ovdje.</em>','booking_banner_p':'Pošaljite datume i broj gostiju. Davor će vam potvrditi raspoloživost i detalje boravka.',
'villa_k':'DOBRO DOŠLI','villa_title':'Privatnost ima svoju <em>adresu.</em>','villa_lead':'Cijela kuća za jednu grupu gostiju. Bez dijeljenih prostora, bez rasporeda i bez nepotrebne žurbe.',
'villa_p1':'Villa Batarelo smještena je u mirnom naselju Lučane, nedaleko od Sinja. S tri spavaće sobe, dnevnim boravkom, kuhinjom i prostorima za boravak na otvorenom, pruža ugodnu bazu za obiteljski odmor ili putovanje s prijateljima.',
'villa_p2':'Posebnu draž daje bazen, vanjski prostor za objedovanje te vrt u kojem se lako zaboravlja na svakodnevni tempo. Domaćin Davor dostupan je za pitanja oko dolaska i boravka.',
'villa_feature_title':'Cijeli prostor. <em>Samo vaš.</em>','villa_feature_text':'Kada rezervirate Villu Batarelo, ne dijelite sadržaje s drugim gostima. Vrijeme uz bazen, večera na terasi i jutarnja kava ostaju potpuno vaši.',
'amenities_k':'PROSTOR I SADRŽAJI','amenities_title':'Udobnost je <em>u detaljima.</em>','amenities_lead':'Od jutarnje kave do večere na terasi — sve je organizirano za opušten boravak.',
'amen_cards':[('Kreveti i odmor','3 spavaće sobe, posteljina i ručnici za goste.','bedroom'),('Dnevni boravak','Ugodan zajednički prostor, televizor i klimatizacija.','inside'),('Kuhinja i objedovanje','Opremljena kuhinja s perilicom posuđa, mikrovalnom pećnicom i aparatima za kavu.','inside'),('Bazen i sunčalište','Privatni vanjski bazen i prostor za boravak uz vodu.','pool'),('Terasa i roštilj','Natkriveni prostor za objedovanje i mogućnost pripreme roštilja.','outside'),('Okućnica','Vrt i uređena livada prikladna i za boravak kućnih ljubimaca.','exterior')],
'amen_list_title':'Još malo udobnosti','amen_list':['Wi-Fi','Klima-uređaji','Besplatan privatni parking','Perilica rublja','Perilica posuđa','Opremljena kuhinja','Vanjski namještaj','Roštilj','Ručnici i posteljina','Kućni ljubimci dobrodošli','Samostalni dolazak uz sef za ključeve','Privatni ulaz'],
'gallery_page_k':'GALERIJA','gallery_page_t':'Pogledajte <em>svaki kutak.</em>','gallery_lead':'Fotografije vile, bazena i prostora za boravak. Postojeće fotografije trenutačno su povezane s javnim oglasima i bit će zamijenjene izvornicima vlasnika.',
'filters':{'all':'Sve fotografije','exterior':'Eksterijer','pool':'Bazen','outside':'Terasa','inside':'Interijer','bedroom':'Spavaće sobe','bathroom':'Kupaonice'},
'location_page_k':'LOKACIJA I IZLETI','location_page_t':'Sinj, Cetina i <em>još toliko toga.</em>','location_lead':'Mirna baza u Lučanima i odlična polazna točka za izlete po dalmatinskom zaleđu.',
'places':[('Sinj','Alkarska tradicija, povijesna jezgra i lokalni restorani.'),('Muzej Sinjske alke','Upoznajte jedinstvenu vitešku tradiciju ovoga kraja.'),('Rijeka Cetina','Priroda, šetnje i aktivnosti uz poznatu dalmatinsku rijeku.'),('Split','Povijesna jezgra, Dioklecijanova palača i gradska šetnica.'),('Omiš','Grad na ušću Cetine, izleti i obalni krajolici.'),('Izvor Cetine','Izlet u posebno vrijedan i fotogeničan prirodni krajolik.')],
'map_button':'Otvori u Google Kartama','map_title':'Pronađite nas','map_note':'Približna lokacija objekta: Lučane 33c, 21230 Sinj, Hrvatska. Za upute do ulaza kontaktirajte domaćina.',
'booking_page_k':'DIREKTAN UPIT','booking_page_t':'Pošaljite nam <em>svoje datume.</em>','booking_lead':'Pošaljite neobvezujući upit. Davor će osobno potvrditi dostupnost, cijenu i detalje boravka. Ovo nije automatska rezervacija.',
'form_title':'Vaš upit za boravak','arrival':'Datum dolaska','departure':'Datum odlaska','guests':'Broj gostiju','name':'Ime i prezime','email':'E-mail adresa','phone':'Broj telefona (neobavezno)','message':'Poruka (neobavezno)','consent':'Slažem se da se navedeni podaci koriste za odgovor na moj upit.','send':'Pošaljite upit putem WhatsAppa','email_option':'Ili pošaljite e-mail','validation':'Provjerite datume, obavezna polja i privolu prije slanja.','sent_note':'Otvara se WhatsApp s pripremljenom porukom. Upit je poslan tek kada ga pošaljete u WhatsAppu.','form_note':'Ne obračunavamo cijenu automatski niti potvrđujemo rezervaciju.','platforms':'Radije koristite platformu za rezervacije?','contact_k':'TU SMO ZA PITANJA','contact_title':'Javite nam se <em>jednostavno.</em>','contact_lead':'Za termine, cijenu i sve pojedinosti boravka javite se izravno domaćinu.',
'call':'Nazovite nas','wa':'Pišite na WhatsApp','address':'Adresa','host':'Domaćin','questions':'Imate pitanje?','faq_t':'Dobro je znati','faq':[('Je li vila samo za našu grupu?','Da. Vila i pripadajući sadržaji iznajmljuju se kao jedna privatna cjelina.'),('Kako mogu provjeriti je li termin slobodan?','Pošaljite upit s datumima. Domaćin će potvrditi raspoloživost i cijenu.'),('Jesu li kućni ljubimci dopušteni?','Prema postojećim oglasima jesu. Prije dolaska navedite da dolazite s ljubimcem.'),('Postoji li parking?','Da, gostima je na raspolaganju besplatan privatni parking.')],
'privacy_title':'Pravila privatnosti','cookies_title':'Pravila kolačića','terms_title':'Uvjeti boravka','legal_notice':'Radni nacrt — vlasnik treba potvrditi službene podatke i uvjete prije javne objave.','privacy_body':['Podaci koje unesete u obrazac koriste se isključivo kako bi domaćin odgovorio na vaš upit. Podaci koje pošaljete putem WhatsAppa ili e-maila obrađuju se i prema pravilima tih pružatelja usluga.','Web stranica ne obrađuje plaćanja i ne potvrđuje rezervacije automatski. Za pitanja o privatnosti obratite se domaćinu putem kontakata na stranici.','Ako se naknadno aktivira analitika, ona će se pokretati tek nakon odgovarajuće privole.'],
'cookies_body':['Stranica koristi lokalnu pohranu za pamćenje vašeg izbora kolačića i za prikaz uvodnog ekrana samo jednom tijekom posjeta.','Neobavezna analitika nije uključena dok se ne konfigurira mjerenje i dok ne date privolu.','Vaše postavke možete izmijeniti putem poveznice „Postavke kolačića” u podnožju stranice.'],
'terms_body':['Slanje upita nije potvrda rezervacije. Dostupnost, konačnu cijenu, način plaćanja i uvjete otkazivanja potvrđuje domaćin prije dogovora o boravku.','Prema javnom oglasu na Bookingu prijava je od 15:00, a odjava do 10:00. Točne uvjete potvrdite s domaćinom.','U objektu nije dopušteno pušenje, a zabave i događanja nisu dopušteni prema objavljenim pravilima. Kućni ljubimci dopušteni su prema javnom oglasu; dolazak s ljubimcem prethodno najavite.'],
'cookie_notice':'Koristimo nužnu lokalnu pohranu, a opcionalnu analitiku samo uz vaš pristanak.','accept':'Prihvati','reject':'Odbij','cookie_settings':'Postavke kolačića','copyright':'Sva prava pridržana.','built':'Web dizajn: Medium29',
},
'en':{
'locale':'en_GB','tagline':'Private pool villa · Lučane near Sinj','nav':{'home':'Home','villa':'The villa','amenities':'Amenities','gallery':'Gallery','location':'Explore','booking':'Availability','contact':'Contact','privacy':'Privacy','cookies':'Cookies','terms':'Stay terms'},
'cta':'Send an enquiry','explore':'Explore the villa','check':'Check availability','view_gallery':'View gallery','learn':'Discover more','see_all':'All photos','view_details':'Explore amenities',
'home_title':'Your space to <em>slow down.</em>','home_sub':'A private pool, generous outdoor living and the peace of Lučane, just outside Sinj. The entire villa is yours.',
'eyebrow':'VILLA BATARELO · SINJ, CROATIA','stats':['3 bedrooms','Private pool','Entire villa','Free parking'],
'home_intro_k':'A DIFFERENT PACE OF LIFE','home_intro_title':'Unhurried days. <em>Room to be together.</em>','home_intro_text':'In Lučane, a short drive from Sinj, Villa Batarelo offers the kind of privacy that is hard to find in busy seaside resorts. Start by the pool, gather for lunch on the terrace and stay outside long after sunset.',
'photo_pool_k':'OUTDOOR LIVING','photo_pool_t':'Poolside afternoons. <em>Long evenings.</em>','photo_pool_p':'Spend the day by the water, prepare dinner on the grill or enjoy a meal beneath the covered terrace. These outdoor spaces are exclusively yours.',
'main_amen_k':'COMFORT FOR EVERYONE','main_amen_t':'Everything you need, <em>right where you are.</em>','amen_short':['Three separate bedrooms for a restful night.','Air-conditioned interiors, a fully equipped kitchen and living area.','Your own pool, dining terrace, barbecue and garden.'],
'gallery_k':'A GLIMPSE INSIDE','gallery_t':'Let the spaces <em>speak for themselves.</em>','location_k':'THE DALMATIAN HINTERLAND','location_t':'Close to places worth seeing. <em>Far from the crowds.</em>','location_p':'Villa Batarelo is in Lučane, around 3.5 km from Sinj. Enjoy quiet countryside surroundings while exploring the Cetina River, local culture and the Dalmatian coast.',
'reviews_k':'GUEST FEEDBACK','reviews_t':'Kind words from <em>past guests.</em>','review_info':'Ratings reflect public listings and may change. Click for the latest guest reviews.',
'booking_banner_k':'READY FOR A BREAK?','booking_banner_t':'Your next stay <em>starts here.</em>','booking_banner_p':'Send your dates and group size. Davor will reply with availability and further details.',
'villa_k':'WELCOME INSIDE','villa_title':'Privacy has <em>an address.</em>','villa_lead':'A complete villa for one group. No shared areas, no rigid schedules, no rush.',
'villa_p1':'Villa Batarelo sits in the quiet village of Lučane near Sinj. With three bedrooms, a living room, a kitchen and generous outdoor areas, it is a comfortable base for families and friends travelling together.',
'villa_p2':'The private pool, dining terrace and garden make it easy to enjoy slow days at home. Your host Davor is available to answer questions before and during your stay.',
'villa_feature_title':'The whole place. <em>All yours.</em>','villa_feature_text':'When you book Villa Batarelo, there are no other guests sharing the facilities. Morning coffee, pool time and meals outdoors are entirely on your terms.',
'amenities_k':'SPACE & COMFORT','amenities_title':'Comfort is in <em>the details.</em>','amenities_lead':'From the first coffee of the day to dinner outside, every space is made for easy living.',
'amen_cards':[('Bedrooms','Three bedrooms with linen and towels for guests.','bedroom'),('Living room','Comfortable shared space with a TV and air-conditioning.','inside'),('Kitchen & dining','Fully equipped kitchen including dishwasher, microwave and coffee makers.','inside'),('Private pool','Outdoor swimming pool with space to unwind nearby.','pool'),('Terrace & barbecue','Covered dining terrace and barbecue facilities.','outside'),('Private grounds','Garden and a grassy area where pets can enjoy the outdoors.','exterior')],
'amen_list_title':'Everything else you need','amen_list':['Wi-Fi','Air-conditioning','Free private parking','Washing machine','Dishwasher','Equipped kitchen','Outdoor furniture','Barbecue','Towels and bed linen','Pets welcome','Self check-in with a lockbox','Private entrance'],
'gallery_page_k':'PHOTO GALLERY','gallery_page_t':'Explore <em>every corner.</em>','gallery_lead':'A closer look at the villa, pool and living spaces. Current images are linked from public listings and will be replaced with the owner’s original files.',
'filters':{'all':'All photos','exterior':'Exterior','pool':'Pool','outside':'Terrace','inside':'Interiors','bedroom':'Bedrooms','bathroom':'Bathrooms'},
'location_page_k':'LOCATION & EXPERIENCES','location_page_t':'Sinj, Cetina and <em>beyond.</em>','location_lead':'A quiet base in Lučane for discovering the landscapes and traditions of the Dalmatian hinterland.',
'places':[('Sinj','Alka heritage, historic streets and local restaurants.'),('Museum of Sinjska Alka','Discover the distinctive equestrian tradition of Sinj.'),('Cetina River','Nature, walking and outdoor activities by the river.'),('Split','The old town, Diocletian’s Palace and the waterfront.'),('Omiš','A coastal town at the mouth of the Cetina River.'),('Cetina Spring','A remarkable natural destination for a day trip.')],
'map_button':'Open in Google Maps','map_title':'Find us','map_note':'Property address: Lučane 33c, 21230 Sinj, Croatia. Contact the host for arrival instructions.',
'booking_page_k':'DIRECT ENQUIRIES','booking_page_t':'Tell us <em>your dates.</em>','booking_lead':'Send a no-obligation enquiry. Davor will personally confirm availability, pricing and stay details. This is not an instant booking.',
'form_title':'Plan your stay','arrival':'Check-in date','departure':'Check-out date','guests':'Number of guests','name':'Full name','email':'Email address','phone':'Phone (optional)','message':'Message (optional)','consent':'I agree that my details may be used to respond to this enquiry.','send':'Send enquiry via WhatsApp','email_option':'Or send by email','validation':'Please check the dates, required fields and consent.','sent_note':'WhatsApp opens with a prepared message. Your enquiry is sent only when you send it there.','form_note':'No automatic pricing or reservation confirmation.','platforms':'Prefer to book through a platform?',
'contact_k':'LET’S TALK','contact_title':'We’re <em>easy to reach.</em>','contact_lead':'For dates, rates or any questions about the villa, contact your host directly.','call':'Call us','wa':'Message on WhatsApp','address':'Address','host':'Your host','questions':'Any questions?','faq_t':'Good to know','faq':[('Will we have the whole villa to ourselves?','Yes. The villa and outdoor facilities are rented as one private property.'),('How can I check dates?','Send your dates in an enquiry. The host will confirm availability and price.'),('Are pets allowed?','According to the current listings, yes. Please let the host know in advance.'),('Is parking available?','Yes, free private parking is available for guests.')],
'privacy_title':'Privacy policy','cookies_title':'Cookie policy','terms_title':'Stay terms','legal_notice':'Draft text — the owner should confirm official business details and stay conditions before publication.',
'privacy_body':['Information you submit in the enquiry form is used only so the host can respond to you. WhatsApp and email communications are also governed by those services’ privacy practices.','This site does not process payments or confirm bookings automatically. Contact the host using the details on this website for privacy enquiries.','If analytics is enabled later, it will only run after appropriate consent is given.'],
'cookies_body':['This website uses local storage to remember your cookie preference and to show the introduction screen only once per session.','Optional analytics is disabled unless configured and consented to.','You can change your choice at any time using “Cookie settings” in the footer.'],
'terms_body':['Sending an enquiry does not confirm a reservation. Availability, final rates, payment details and cancellation conditions are confirmed by the host before a stay is agreed.','According to the public Booking listing, check-in starts at 15:00 and check-out is by 10:00. Confirm exact arrangements with your host.','Smoking and parties are not allowed according to the published rules. Pets are allowed according to the public listing; please tell the host before arriving.'],
'cookie_notice':'We use essential local storage and optional analytics only with your consent.','accept':'Accept','reject':'Reject','cookie_settings':'Cookie settings','copyright':'All rights reserved.','built':'Website by Medium29',
},
'de':{
'locale':'de_DE','tagline':'Private Villa mit Pool · Lučane bei Sinj','nav':{'home':'Startseite','villa':'Die Villa','amenities':'Ausstattung','gallery':'Galerie','location':'Umgebung','booking':'Verfügbarkeit','contact':'Kontakt','privacy':'Datenschutz','cookies':'Cookies','terms':'Aufenthaltsregeln'},
'cta':'Anfrage senden','explore':'Villa entdecken','check':'Verfügbarkeit anfragen','view_gallery':'Galerie ansehen','learn':'Mehr erfahren','see_all':'Alle Fotos','view_details':'Ausstattung entdecken',
'home_title':'Ihr Rückzugsort <em>zum Durchatmen.</em>','home_sub':'Privater Pool, großzügige Außenbereiche und die Ruhe von Lučane – nur wenige Kilometer von Sinj entfernt. Die gesamte Villa gehört Ihnen.',
'eyebrow':'VILLA BATARELO · SINJ, KROATIEN','stats':['3 Schlafzimmer','Privater Pool','Ganze Villa','Kostenloser Parkplatz'],
'home_intro_k':'ZEIT FÜR RUHE','home_intro_title':'Weniger Termine. <em>Mehr gemeinsame Zeit.</em>','home_intro_text':'In Lučane, unweit von Sinj, bietet die Villa Batarelo die Privatsphäre, die an belebten Urlaubsorten oft fehlt. Beginnen Sie den Tag am Pool, genießen Sie das Essen auf der Terrasse und bleiben Sie bis in den Abend draußen.',
'photo_pool_k':'DRAUSSEN ZU HAUSE','photo_pool_t':'Am Pool entspannen. <em>Den Abend genießen.</em>','photo_pool_p':'Verbringen Sie den Tag am Wasser, grillen Sie gemeinsam oder essen Sie auf der überdachten Terrasse. Die Außenbereiche stehen ausschließlich Ihrer Gruppe zur Verfügung.',
'main_amen_k':'KOMFORT FÜR ALLE','main_amen_t':'Alles für Ihren Aufenthalt. <em>An einem Ort.</em>','amen_short':['Drei separate Schlafzimmer für erholsame Nächte.','Klimatisierte Räume, voll ausgestattete Küche und Wohnbereich.','Eigener Pool, Essbereich im Freien, Grill und Garten.'],
'gallery_k':'EIN BLICK IN DIE VILLA','gallery_t':'Räume, die <em>für sich sprechen.</em>','location_k':'DALMATINISCHES HINTERLAND','location_t':'Viel zu entdecken. <em>Weit weg vom Trubel.</em>','location_p':'Die Villa Batarelo liegt in Lučane, rund 3,5 km von Sinj entfernt. Genießen Sie die Ruhe der Natur und entdecken Sie die Cetina, die Kultur der Region und die dalmatinische Küste.',
'reviews_k':'GÄSTEBEWERTUNGEN','reviews_t':'Was unsere Gäste <em>schätzen.</em>','review_info':'Bewertungen stammen aus öffentlichen Inseraten und können sich ändern. Klicken Sie für die aktuellen Bewertungen.',
'booking_banner_k':'URLAUB GEPLANT?','booking_banner_t':'Ihre Auszeit <em>beginnt hier.</em>','booking_banner_p':'Senden Sie uns Ihre Reisedaten und die Gästezahl. Davor bestätigt Verfügbarkeit und Details persönlich.',
'villa_k':'HERZLICH WILLKOMMEN','villa_title':'Privatsphäre hat <em>eine Adresse.</em>','villa_lead':'Ein ganzes Ferienhaus für Ihre Gruppe. Keine geteilten Bereiche, keine festen Tagespläne, keine Hektik.',
'villa_p1':'Die Villa Batarelo liegt im ruhigen Ort Lučane nahe Sinj. Mit drei Schlafzimmern, Wohnzimmer, Küche und großzügigen Außenbereichen ist sie ideal für Familien und Freunde, die gemeinsam reisen.',
'villa_p2':'Der private Pool, die Terrasse und der Garten laden zu entspannten Tagen ein. Gastgeber Davor beantwortet gerne Ihre Fragen vor und während des Aufenthalts.',
'villa_feature_title':'Die ganze Villa. <em>Nur für Sie.</em>','villa_feature_text':'Während Ihres Aufenthalts teilen Sie Pool, Terrasse und Garten nicht mit anderen Gästen. Genießen Sie Ihren Urlaub ganz nach Ihrem eigenen Rhythmus.',
'amenities_k':'RÄUME & AUSSTATTUNG','amenities_title':'Komfort zeigt sich <em>im Detail.</em>','amenities_lead':'Vom ersten Kaffee bis zum Abendessen auf der Terrasse – hier können Sie den Tag entspannt gestalten.',
'amen_cards':[('Schlafzimmer','Drei Schlafzimmer mit Bettwäsche und Handtüchern.','bedroom'),('Wohnbereich','Gemütlicher Wohnbereich mit Fernseher und Klimaanlage.','inside'),('Küche & Essen','Voll ausgestattete Küche mit Geschirrspüler, Mikrowelle und Kaffeemaschinen.','inside'),('Privater Pool','Außenpool mit Platz zum Entspannen am Wasser.','pool'),('Terrasse & Grill','Überdachter Essbereich im Freien mit Grillmöglichkeit.','outside'),('Grundstück','Garten und gepflegte Grünfläche, auch für Haustiere geeignet.','exterior')],
'amen_list_title':'Gut ausgestattet','amen_list':['WLAN','Klimaanlage','Kostenloser Privatparkplatz','Waschmaschine','Geschirrspüler','Ausgestattete Küche','Gartenmöbel','Grill','Handtücher und Bettwäsche','Haustiere willkommen','Self-Check-in mit Schlüsselsafe','Privater Eingang'],
'gallery_page_k':'FOTOGALERIE','gallery_page_t':'Entdecken Sie <em>jeden Winkel.</em>','gallery_lead':'Ein Einblick in Villa, Pool und Wohnbereiche. Aktuelle Bilder werden vorübergehend aus öffentlichen Inseraten eingebunden und später durch Originaldateien des Eigentümers ersetzt.',
'filters':{'all':'Alle Fotos','exterior':'Außenansicht','pool':'Pool','outside':'Terrasse','inside':'Innenräume','bedroom':'Schlafzimmer','bathroom':'Badezimmer'},
'location_page_k':'LAGE & AUSFLÜGE','location_page_t':'Sinj, Cetina und <em>viel mehr.</em>','location_lead':'Ein ruhiger Ausgangspunkt in Lučane für Entdeckungen im dalmatinischen Hinterland.',
'places':[('Sinj','Alka-Tradition, historische Gassen und regionale Restaurants.'),('Museum der Sinjska Alka','Entdecken Sie die besondere Reitertradition von Sinj.'),('Fluss Cetina','Natur, Spaziergänge und Aktivitäten am Wasser.'),('Split','Altstadt, Diokletianpalast und die Hafenpromenade.'),('Omiš','Küstenstadt an der Mündung des Flusses Cetina.'),('Cetina-Quelle','Ein außergewöhnliches Naturziel für einen Tagesausflug.')],
'map_button':'In Google Maps öffnen','map_title':'So finden Sie uns','map_note':'Adresse: Lučane 33c, 21230 Sinj, Kroatien. Fragen Sie den Gastgeber nach der genauen Anfahrt.',
'booking_page_k':'DIREKTE ANFRAGE','booking_page_t':'Nennen Sie uns <em>Ihre Reisedaten.</em>','booking_lead':'Senden Sie eine unverbindliche Anfrage. Davor bestätigt Verfügbarkeit, Preis und Einzelheiten persönlich. Dies ist keine sofortige Buchung.',
'form_title':'Aufenthalt anfragen','arrival':'Anreise','departure':'Abreise','guests':'Anzahl der Gäste','name':'Vor- und Nachname','email':'E-Mail-Adresse','phone':'Telefon (optional)','message':'Nachricht (optional)','consent':'Ich bin damit einverstanden, dass meine Angaben zur Beantwortung meiner Anfrage verwendet werden.','send':'Anfrage über WhatsApp senden','email_option':'Oder per E-Mail senden','validation':'Bitte prüfen Sie die Reisedaten, Pflichtfelder und Einwilligung.','sent_note':'WhatsApp öffnet sich mit einer vorbereiteten Nachricht. Die Anfrage wird erst gesendet, wenn Sie sie dort abschicken.','form_note':'Keine automatische Preisberechnung oder Buchungsbestätigung.','platforms':'Möchten Sie lieber über eine Plattform buchen?',
'contact_k':'WIR SIND FÜR SIE DA','contact_title':'Kontaktieren Sie uns <em>ganz einfach.</em>','contact_lead':'Bei Fragen zu Terminen, Preisen und Ihrem Aufenthalt wenden Sie sich direkt an Ihren Gastgeber.','call':'Jetzt anrufen','wa':'WhatsApp-Nachricht','address':'Adresse','host':'Gastgeber','questions':'Noch Fragen?','faq_t':'Gut zu wissen','faq':[('Ist die Villa nur für unsere Gruppe?','Ja. Die Villa und ihre Außenbereiche werden als eine private Unterkunft vermietet.'),('Wie frage ich nach freien Terminen?','Schicken Sie uns Ihre Reisedaten. Der Gastgeber bestätigt Verfügbarkeit und Preis.'),('Sind Haustiere erlaubt?','Laut aktuellen Inseraten ja. Informieren Sie bitte den Gastgeber vorab.'),('Gibt es Parkplätze?','Ja, kostenlose private Parkplätze stehen zur Verfügung.')],
'privacy_title':'Datenschutzerklärung','cookies_title':'Cookie-Richtlinie','terms_title':'Aufenthaltsbedingungen','legal_notice':'Entwurf — Eigentümer muss offizielle Angaben und Bedingungen vor Veröffentlichung bestätigen.',
'privacy_body':['Ihre Angaben aus dem Anfrageformular dienen ausschließlich dazu, Ihre Anfrage zu beantworten. Für Nachrichten über WhatsApp oder E-Mail gelten zusätzlich die Datenschutzregeln der jeweiligen Anbieter.','Diese Website verarbeitet keine Zahlungen und bestätigt Buchungen nicht automatisch. Datenschutzanfragen richten Sie bitte an den Gastgeber.','Eine optionale Analysefunktion wird erst nach Konfiguration und Ihrer Zustimmung aktiviert.'],
'cookies_body':['Diese Website nutzt lokale Speicherung, um Ihre Cookie-Auswahl zu speichern und das Intro nur einmal pro Sitzung anzuzeigen.','Optionale Analysedienste bleiben deaktiviert, solange sie nicht eingerichtet und von Ihnen akzeptiert wurden.','Ihre Entscheidung können Sie jederzeit über „Cookie-Einstellungen“ im Footer ändern.'],
'terms_body':['Eine Anfrage ist keine Buchungsbestätigung. Verfügbarkeit, Endpreis, Zahlungsweise und Stornierungsbedingungen bestätigt der Gastgeber vor der verbindlichen Vereinbarung.','Laut öffentlichem Booking-Inserat ist der Check-in ab 15:00 Uhr und der Check-out bis 10:00 Uhr. Bitte klären Sie Details mit dem Gastgeber.','Rauchen sowie Partys und Veranstaltungen sind laut veröffentlichten Regeln nicht gestattet. Haustiere sind laut Inserat erlaubt; melden Sie diese bitte vorher an.'],
'cookie_notice':'Wir nutzen notwendige lokale Speicherung und optionale Analytik nur mit Einwilligung.','accept':'Akzeptieren','reject':'Ablehnen','cookie_settings':'Cookie-Einstellungen','copyright':'Alle Rechte vorbehalten.','built':'Webdesign: Medium29',
}}
# Medium29 content revision: natural language, specific headings and consistent translations.
LANGS['hr'].update({
 'home_title':'Privatna vila s <em>bazenom kod Sinja.</em>',
 'home_sub':'Villa Batarelo nalazi se u Lučanima, blizu Sinja. Na raspolaganju su vam cijela kuća, privatni bazen i terasa.',
 'home_intro_k':'O VILI','home_intro_title':'Villa Batarelo u Lučanima',
 'home_intro_text':'Vila ima tri spavaće sobe, dnevni boravak, kuhinju i prostor za druženje na otvorenom. Iznajmljuje se kao cjelina, tako da bazen i terasa ostaju samo vama na raspolaganju.',
 'photo_pool_k':'BAZEN I TERASA','photo_pool_t':'Privatni bazen i terasa',
 'photo_pool_p':'Vrijeme možete provesti uz bazen, na natkrivenoj terasi ili uz roštilj. Vanjski sadržaji pripadaju gostima vile.',
 'main_amen_k':'SMJEŠTAJ','main_amen_t':'Sve za ugodan boravak',
 'gallery_k':'FOTOGRAFIJE','gallery_t':'Pogledajte Villu Batarelo',
 'location_k':'LOKACIJA','location_t':'Lučane, blizu Sinja',
 'location_p':'Villa Batarelo nalazi se u Lučanima, u dalmatinskom zaleđu. Sinj, rijeka Cetina i brojne mogućnosti za izlete dostupni su gostima koji žele istražiti okolicu.',
 'reviews_k':'RECENZIJE','reviews_t':'Ocjene gostiju',
 'booking_banner_k':'REZERVACIJE','booking_banner_t':'Provjerite slobodne termine',
 'booking_banner_p':'Pošaljite datume dolaska i odlaska. Davor će vam odgovoriti s informacijama o dostupnosti i cijeni.',
 'villa_k':'O VILI','villa_title':'Upoznajte Villu Batarelo',
 'villa_lead':'Privatna kuća za odmor s tri spavaće sobe, bazenom i vlastitim vanjskim prostorom u Lučanima.',
 'villa_feature_title':'Cijela vila samo za vas',
 'amenities_k':'SMJEŠTAJ I OPREMA','amenities_title':'Sadržaji Ville Batarelo',
 'amenities_lead':'Pregled unutarnjeg i vanjskog prostora te opreme koja je na raspolaganju gostima.',
 'amen_cards':[('Spavaće sobe','Tri spavaće sobe te posteljina i ručnici za goste.','bedroom'),('Dnevni boravak','Prostor za zajednički boravak s televizorom i klimatizacijom.','inside'),('Kuhinja i blagovaonica','Kuhinja s perilicom posuđa, mikrovalnom pećnicom i opremom za pripremu jela.','inside'),('Privatni bazen','Vanjski bazen namijenjen isključivo gostima vile.','pool'),('Terasa i roštilj','Natkriveni prostor za objedovanje i roštilj.','outside'),('Vrt i okućnica','Privatni vanjski prostor oko kuće.','exterior')],
 'amen_list_title':'Oprema i pogodnosti',
 'gallery_page_k':'GALERIJA','gallery_page_t':'Fotografije vile',
 'gallery_lead':'Fotografije bazena, interijera i vanjskog prostora Ville Batarelo.',
 'location_page_k':'LOKACIJA','location_page_t':'Sinj i okolica',
 'location_lead':'Upoznajte grad Sinj, rijeku Cetinu i nekoliko zanimljivih mjesta za izlet iz Lučana.',
 'places':[('Sinj','Povijesna jezgra, znamenitosti i restorani u gradu poznatom po Sinjskoj alki.','Sinj Hrvatska'),('Muzej Sinjske alke','Stalni postav posvećen tradiciji Sinjske alke.','Muzej Sinjske alke Sinj'),('Rijeka Cetina','Rijeka i okolni krajolik pružaju brojne mogućnosti za boravak u prirodi.','rijeka Cetina Sinj'),('Split','Dioklecijanova palača, stara gradska jezgra i šetnica uz more.','Split stari grad Hrvatska'),('Omiš','Grad na ušću Cetine s povijesnom jezgrom i plažama.','Omiš Hrvatska'),('Izvor Cetine','Poznati prirodni izvor rijeke Cetine, popularno izletište.','Izvor Cetine Vrlika Hrvatska')],
 'map_title':'Kako do vile','map_note':'Villa Batarelo, Lučane 33c, 21230 Sinj. Kartu možete otvoriti ovdje ili u Google Kartama.',
 'booking_page_k':'UPIT ZA BORAVAK','booking_page_t':'Upit za slobodne termine',
 'booking_lead':'Odaberite datume i pošaljite upit putem WhatsAppa ili e-maila. Davor će potvrditi dostupnost i cijenu; obrazac ne potvrđuje rezervaciju.',
 'form_title':'Odaberite datume','booking_info_title':'Kontaktirajte domaćina','meta_privacy':'Kako se obrađuju osobni podaci gostiju na stranici Villa Batarelo.','meta_cookies':'Informacije o lokalnoj pohrani, kolačićima i postavkama privatnosti.','meta_terms':'Informacije o slanju upita, rezervaciji i pravilima boravka u Villi Batarelo.','form_note':'Upit nije potvrda rezervacije.',
 'contact_k':'KONTAKT','contact_title':'Kontakt i upiti','contact_lead':'Za termine, cijenu i pitanja o smještaju kontaktirajte Davora izravno.',
 'faq_t':'Česta pitanja',
 'legal_notice':'Informacije za goste Ville Batarelo.',
 'privacy_body':[
  'Kada nam se obratite putem WhatsAppa, e-maila ili obrasca za pripremu poruke, koristimo podatke koje nam pošaljete (ime, kontakt, željeni datumi i sadržaj upita) kako bismo odgovorili na vaš upit o smještaju.',
  'Obrazac na ovoj stranici ne sprema podatke na poslužitelj: nakon provjere podataka otvara WhatsApp ili vaš program za e-mail, gdje sami odlučujete hoćete li poslati poruku. Za obradu poruka putem tih usluga vrijede i njihova pravila privatnosti.',
  'Podatke iz zaprimljenog upita koristimo za komunikaciju u vezi s mogućim boravkom i ne prodajemo ih. Za informacije o pristupu, ispravku ili brisanju podataka javite se na kontakt naveden niže.',
  'Opcionalna analitika nije aktivna dok se ne konfigurira i dok korisnik ne da odgovarajuću privolu. Vanjska Google karta učitava se tek na vaš izričit klik.'
 ],
 'cookies_body':[
  'Stranica koristi nužnu pohranu u pregledniku za pamćenje izbora u banneru kolačića (localStorage) i za jednokratni prikaz uvodnog ekrana tijekom sesije (sessionStorage).',
  'Opcionalna Google Analytics analitika trenutačno nije konfigurirana. Ako se naknadno uključi, pokretat će se samo nakon prihvaćanja opcionalnih kolačića.',
  'Google Maps karta ne učitava se automatski. Otvara se tek kada odaberete prikaz karte, pri čemu Google može obrađivati tehničke podatke prema svojim pravilima.',
  'Izbor možete promijeniti klikom na „Postavke kolačića” u podnožju stranice.'
 ],
 'terms_body':[
  'Slanje upita putem web stranice ne predstavlja potvrđenu rezervaciju. Davor potvrđuje dostupnost, konačnu cijenu, eventualni predujam te uvjete promjene ili otkazivanja prije dogovora o boravku.',
  'Prema postojećem oglasu na Bookingu prijava je od 15:00, a odjava do 10:00. Eventualni drukčiji dogovor potrebno je potvrditi s domaćinom prije dolaska.',
  'Prema javno objavljenim pravilima u objektu nije dopušteno pušenje, zabave ni događanja. Kućni ljubimci dopušteni su prema oglasu; njihov dolazak preporučujemo najaviti unaprijed.',
  'Uvjeti rezervacije putem Bookinga ili Airbnba određeni su pravilima i konkretnom ponudom prikazanom na odabranoj platformi.'
 ],
 'scroll_hint':'Više o vili','footer_explore':'Istražite','footer_contact':'Kontakt','footer_bookings':'Rezervacije','footer_email':'E-mail','lang_switch_label':'Odabir jezika','menu_label':'Otvori izbornik','filter_label':'Kategorije fotografija',
 'map_load':'Prikaži Google kartu','map_notice':'Karta će se učitati s Google Maps servisa tek nakon vašeg klika.','place_action':'Prikaži na karti',
 'photo_unavailable':'Fotografije trenutačno nisu dostupne. Pogledajte slike na Bookingu ili Airbnbu.','lightbox_title':'Pregled fotografije',
 'lightbox_close':'Zatvori fotografiju','lightbox_prev':'Prethodna fotografija','lightbox_next':'Sljedeća fotografija'
})
LANGS['en'].update({
 'home_title':'Private pool villa <em>near Sinj.</em>',
 'home_sub':'Villa Batarelo is in Lučane near Sinj, Croatia. Enjoy the entire villa, private pool and outdoor terrace.',
 'home_intro_k':'THE VILLA','home_intro_title':'Villa Batarelo in Lučane',
 'home_intro_text':'Three bedrooms, a living room, kitchen and outdoor dining area make this a practical choice for families or friends. The whole property is rented to one group, including the pool and terrace.',
 'photo_pool_k':'POOL & TERRACE','photo_pool_t':'A private pool and terrace',
 'photo_pool_p':'Spend time by the pool, enjoy meals on the covered terrace or use the barbecue. The outdoor areas are for villa guests only.',
 'main_amen_k':'ACCOMMODATION','main_amen_t':'Everything for a comfortable stay',
 'gallery_k':'PHOTOS','gallery_t':'Inside Villa Batarelo',
 'location_k':'LOCATION','location_t':'Lučane, near Sinj',
 'location_p':'The villa is in Lučane in the Dalmatian hinterland, with Sinj, the Cetina River and opportunities for day trips within reach.',
 'reviews_k':'REVIEWS','reviews_t':'Guest ratings',
 'booking_banner_k':'ENQUIRIES','booking_banner_t':'Ask about available dates',
 'booking_banner_p':'Send your check-in and check-out dates. Davor will reply with availability and prices.',
 'villa_k':'THE VILLA','villa_title':'Get to know Villa Batarelo',
 'villa_lead':'A private holiday villa with three bedrooms, a pool and outdoor space in Lučane.',
 'villa_feature_title':'The entire villa is yours',
 'amenities_k':'ACCOMMODATION','amenities_title':'Villa amenities',
 'amenities_lead':'A look at the rooms, outdoor areas and facilities available to guests.',
 'amen_cards':[('Bedrooms','Three bedrooms, with bed linen and towels for guests.','bedroom'),('Living room','Shared lounge with television and air conditioning.','inside'),('Kitchen & dining','Kitchen with dishwasher, microwave and cooking equipment.','inside'),('Private pool','Outdoor swimming pool reserved for villa guests.','pool'),('Terrace & barbecue','Covered dining area with a barbecue.','outside'),('Garden','Private outdoor space around the house.','exterior')],
 'amen_list_title':'Facilities',
 'gallery_page_k':'GALLERY','gallery_page_t':'Villa photos',
 'gallery_lead':'Photos of the pool, interiors and outdoor areas at Villa Batarelo.',
 'location_page_k':'LOCATION','location_page_t':'Sinj and the surrounding area',
 'location_lead':'Explore Sinj, the Cetina River and places worth visiting from Lučane.',
 'places':[('Sinj','Historic streets, local restaurants and the town’s Alka heritage.','Sinj Croatia'),('Sinjska Alka Museum','A museum dedicated to Sinj’s distinctive equestrian tradition.','Muzej Sinjske alke Sinj'),('Cetina River','Riverside scenery and outdoor activities in the surrounding countryside.','rijeka Cetina Sinj'),('Split','Diocletian’s Palace, the old town and the waterfront.','Split old town Croatia'),('Omiš','A coastal town at the mouth of the Cetina River.','Omiš Croatia'),('Cetina Spring','A natural spring and a popular destination for a day trip.','Izvor Cetine Vrlika Croatia')],
 'map_title':'Find the villa','map_note':'Villa Batarelo, Lučane 33c, 21230 Sinj, Croatia. View the location on the map or open directions.',
 'booking_page_k':'ENQUIRIES','booking_page_t':'Check available dates',
 'booking_lead':'Select your dates and send an enquiry on WhatsApp or by email. Davor will confirm availability and the rate; this is not a confirmed booking.',
 'form_title':'Select your dates','booking_info_title':'Contact your host','meta_privacy':'How guest personal information is handled on the Villa Batarelo website.','meta_cookies':'Details about browser storage, cookies and privacy choices.','meta_terms':'Information about enquiries, booking arrangements and house rules.','form_note':'An enquiry is not a confirmed booking.',
 'contact_k':'CONTACT','contact_title':'Contact & enquiries','contact_lead':'For available dates, prices and questions about your stay, contact Davor directly.',
 'faq_t':'Frequently asked questions',
 'legal_notice':'Information for Villa Batarelo guests.',
 'privacy_body':[
  'When you contact us by WhatsApp, email or the enquiry form, we use the details you choose to send (name, contact details, travel dates and your message) to reply to your accommodation enquiry.',
  'The form does not store your details on a web server. It prepares a message in WhatsApp or your email application; you decide whether to send it. Those services have their own privacy policies.',
  'Enquiry details are used to communicate about your potential stay and are not sold. Contact us using the details below to ask about access, correction or deletion of your personal data.',
  'Optional analytics remains off unless configured and consented to. Google Maps is loaded only when you explicitly choose to display the map.'
 ],
 'cookies_body':[
  'This website uses essential browser storage to remember your cookie-banner choice (localStorage) and to show the introduction animation only once per session (sessionStorage).',
  'Optional Google Analytics is not currently configured. If it is enabled later, it will run only after you accept optional cookies.',
  'Google Maps is not loaded automatically. It loads after you select the map; Google may then process technical information under its own policies.',
  'You can revisit your choice using “Cookie settings” in the footer.'
 ],
 'terms_body':[
  'Sending an enquiry is not a confirmed booking. Davor confirms availability, the total price, any deposit and the cancellation or modification terms before a stay is agreed.',
  'According to the public Booking listing, check-in begins at 15:00 and check-out is by 10:00. Please confirm any alternative arrangements with the host in advance.',
  'According to published house rules, smoking, parties and events are not permitted. Pets are allowed as listed; please notify your host before arriving with an animal.',
  'Bookings made through Booking.com or Airbnb are subject to the specific offer and rules displayed by those platforms.'
 ],
 'scroll_hint':'Discover the villa','footer_explore':'Explore','footer_contact':'Contact','footer_bookings':'Bookings','footer_email':'Email',
 'lang_switch_label':'Choose language','menu_label':'Open menu','filter_label':'Photo categories',
 'map_load':'Show Google map','map_notice':'The map will load from Google Maps only after you click.','place_action':'View on map',
 'photo_unavailable':'Photos are temporarily unavailable. You can view the villa on Booking.com or Airbnb.','lightbox_title':'Photo viewer',
 'lightbox_close':'Close photo','lightbox_prev':'Previous photo','lightbox_next':'Next photo'
})
LANGS['de'].update({
 'home_title':'Private Villa mit Pool <em>bei Sinj.</em>',
 'home_sub':'Die Villa Batarelo liegt in Lučane bei Sinj. Das gesamte Haus, der private Pool und die Terrasse stehen Ihnen zur Verfügung.',
 'home_intro_k':'DIE VILLA','home_intro_title':'Villa Batarelo in Lučane',
 'home_intro_text':'Drei Schlafzimmer, ein Wohnbereich, eine Küche und ein Essplatz im Freien bieten Platz für einen gemeinsamen Aufenthalt. Die gesamte Villa einschließlich Pool und Terrasse wird an eine Gruppe vermietet.',
 'photo_pool_k':'POOL & TERRASSE','photo_pool_t':'Privater Pool und Terrasse',
 'photo_pool_p':'Genießen Sie den Pool, essen Sie auf der überdachten Terrasse oder nutzen Sie den Grill. Die Außenbereiche stehen ausschließlich den Gästen der Villa zur Verfügung.',
 'main_amen_k':'UNTERKUNFT','main_amen_t':'Alles für einen angenehmen Aufenthalt',
 'gallery_k':'FOTOS','gallery_t':'Einblicke in die Villa Batarelo',
 'location_k':'LAGE','location_t':'Lučane, nahe Sinj',
 'location_p':'Die Villa liegt in Lučane im dalmatinischen Hinterland. Sinj, der Fluss Cetina und verschiedene Ausflugsziele liegen in der Umgebung.',
 'reviews_k':'BEWERTUNGEN','reviews_t':'Gästebewertungen',
 'booking_banner_k':'ANFRAGEN','booking_banner_t':'Verfügbarkeit anfragen',
 'booking_banner_p':'Teilen Sie uns Ihre Reisedaten mit. Davor antwortet mit Informationen zu freien Terminen und Preisen.',
 'villa_k':'DIE VILLA','villa_title':'Die Villa Batarelo kennenlernen',
 'villa_lead':'Privates Ferienhaus mit drei Schlafzimmern, Pool und Außenbereich in Lučane.',
 'villa_feature_title':'Die gesamte Villa gehört Ihnen',
 'amenities_k':'UNTERKUNFT','amenities_title':'Ausstattung der Villa',
 'amenities_lead':'Ein Überblick über die Zimmer, den Außenbereich und die Ausstattung für Gäste.',
 'amen_cards':[('Schlafzimmer','Drei Schlafzimmer mit Bettwäsche und Handtüchern.','bedroom'),('Wohnbereich','Gemeinschaftlicher Wohnraum mit Fernseher und Klimaanlage.','inside'),('Küche & Essbereich','Küche mit Geschirrspüler, Mikrowelle und Kochzubehör.','inside'),('Privater Pool','Außenpool ausschließlich für Gäste der Villa.','pool'),('Terrasse & Grill','Überdachter Essplatz mit Grill.','outside'),('Garten','Privater Außenbereich rund um das Haus.','exterior')],
 'amen_list_title':'Weitere Ausstattung',
 'gallery_page_k':'GALERIE','gallery_page_t':'Fotos der Villa',
 'gallery_lead':'Fotos vom Pool, den Innenräumen und dem Außenbereich der Villa Batarelo.',
 'location_page_k':'LAGE','location_page_t':'Sinj und Umgebung',
 'location_lead':'Entdecken Sie Sinj, den Fluss Cetina und lohnende Ausflugsziele rund um Lučane.',
 'places':[('Sinj','Historische Gassen, lokale Restaurants und die Tradition der Sinjska Alka.','Sinj Kroatien'),('Museum der Sinjska Alka','Ausstellung zur Reitertradition von Sinj.','Muzej Sinjske alke Sinj'),('Fluss Cetina','Flusslandschaft und Freizeitmöglichkeiten in der Natur.','rijeka Cetina Sinj'),('Split','Diokletianpalast, Altstadt und Uferpromenade.','Split Altstadt Kroatien'),('Omiš','Küstenstadt an der Mündung des Flusses Cetina.','Omiš Kroatien'),('Cetina-Quelle','Naturquelle und beliebtes Ausflugsziel.','Izvor Cetine Vrlika Kroatien')],
 'map_title':'So finden Sie uns','map_note':'Villa Batarelo, Lučane 33c, 21230 Sinj, Kroatien. Sehen Sie sich die Lage auf der Karte an.',
 'booking_page_k':'ANFRAGE','booking_page_t':'Freie Termine anfragen',
 'booking_lead':'Wählen Sie Ihre Reisedaten und senden Sie eine Anfrage über WhatsApp oder E-Mail. Davor bestätigt Verfügbarkeit und Preis; dies ist keine verbindliche Buchung.',
 'form_title':'Reisedaten wählen','booking_info_title':'Gastgeber kontaktieren','meta_privacy':'Informationen zur Verarbeitung persönlicher Daten auf der Website der Villa Batarelo.','meta_cookies':'Hinweise zur Browserspeicherung, zu Cookies und Datenschutzeinstellungen.','meta_terms':'Informationen zu Anfragen, Buchungen und Hausregeln in der Villa Batarelo.','form_note':'Eine Anfrage ist noch keine bestätigte Buchung.',
 'contact_k':'KONTAKT','contact_title':'Kontakt & Anfragen','contact_lead':'Bei Fragen zu Terminen, Preisen und Unterkunft wenden Sie sich direkt an Davor.',
 'faq_t':'Häufige Fragen',
 'legal_notice':'Informationen für Gäste der Villa Batarelo.',
 'privacy_body':[
  'Wenn Sie uns über WhatsApp, E-Mail oder das Anfrageformular kontaktieren, verwenden wir die von Ihnen übermittelten Daten (Name, Kontaktdaten, Reisedaten und Nachricht), um Ihre Anfrage zu beantworten.',
  'Das Formular speichert Ihre Daten nicht auf einem Webserver. Es bereitet eine Nachricht in WhatsApp oder Ihrem E-Mail-Programm vor. Ob Sie diese Nachricht absenden, entscheiden Sie selbst. Für diese Dienste gelten auch deren Datenschutzbestimmungen.',
  'Die Angaben werden zur Kommunikation über einen möglichen Aufenthalt verwendet und nicht verkauft. Für Anfragen zu Auskunft, Berichtigung oder Löschung wenden Sie sich bitte an die unten angegebenen Kontaktdaten.',
  'Optionale Analysen bleiben deaktiviert, bis sie eingerichtet wurden und eine entsprechende Einwilligung vorliegt. Google Maps wird erst nach Ihrer ausdrücklichen Auswahl geladen.'
 ],
 'cookies_body':[
  'Diese Website verwendet notwendige Browserspeicherung, um Ihre Cookie-Einstellung (localStorage) zu speichern und die Intro-Animation nur einmal je Sitzung anzuzeigen (sessionStorage).',
  'Google Analytics ist derzeit nicht eingerichtet. Bei späterer Aktivierung wird es erst nach Zustimmung zu optionalen Cookies geladen.',
  'Google Maps wird nicht automatisch geladen. Erst wenn Sie die Karte öffnen, werden Inhalte von Google nachgeladen. Google kann dabei technische Daten nach den eigenen Datenschutzbestimmungen verarbeiten.',
  'Sie können Ihre Auswahl jederzeit über „Cookie-Einstellungen” in der Fußzeile ändern.'
 ],
 'terms_body':[
  'Eine Anfrage stellt keine bestätigte Buchung dar. Davor bestätigt Verfügbarkeit, Gesamtpreis, mögliche Anzahlungen sowie Umbuchungs- und Stornierungsbedingungen vor einer verbindlichen Vereinbarung.',
  'Laut dem veröffentlichten Booking-Angebot ist der Check-in ab 15:00 Uhr und der Check-out bis 10:00 Uhr möglich. Abweichungen müssen vorab mit dem Gastgeber abgestimmt werden.',
  'Laut den veröffentlichten Hausregeln sind Rauchen, Partys und Veranstaltungen nicht erlaubt. Haustiere sind laut Angebot erlaubt; informieren Sie den Gastgeber bitte vor der Anreise.',
  'Für Buchungen über Booking.com oder Airbnb gelten die jeweiligen Angebotsbedingungen der Plattformen.'
 ],
 'scroll_hint':'Villa entdecken','footer_explore':'Entdecken','footer_contact':'Kontakt','footer_bookings':'Buchung','footer_email':'E-Mail',
 'lang_switch_label':'Sprache auswählen','menu_label':'Menü öffnen','filter_label':'Fotokategorien',
 'map_load':'Google-Karte anzeigen','map_notice':'Die Google-Karte wird erst nach einem Klick geladen.','place_action':'Auf Karte ansehen',
 'photo_unavailable':'Fotos sind vorübergehend nicht verfügbar. Besuchen Sie unser Profil auf Booking.com oder Airbnb.','lightbox_title':'Fotoansicht',
 'lightbox_close':'Foto schließen','lightbox_prev':'Vorheriges Foto','lightbox_next':'Nächstes Foto'
})

PAGES=['home','villa','amenities','gallery','location','booking','contact','privacy','cookies','terms']
PICALT={
'hr':{'exterior':'Pogled na Villu Batarelo i privatni bazen u Lučanima','pool':'Privatni bazen Ville Batarelo','outside':'Natkrivena terasa Ville Batarelo','inside':'Interijer i dnevni prostor Ville Batarelo','bedroom':'Spavaća soba Ville Batarelo','bathroom':'Kupaonica Ville Batarelo'},
'en':{'exterior':'Villa Batarelo house and private pool in Lučane','pool':'Private pool at Villa Batarelo','outside':'Covered outdoor terrace at Villa Batarelo','inside':'Living spaces at Villa Batarelo','bedroom':'Bedroom at Villa Batarelo','bathroom':'Bathroom at Villa Batarelo'},
'de':{'exterior':'Villa Batarelo mit privatem Pool in Lučane','pool':'Privater Pool der Villa Batarelo','outside':'Überdachte Terrasse der Villa Batarelo','inside':'Wohnbereich der Villa Batarelo','bedroom':'Schlafzimmer der Villa Batarelo','bathroom':'Badezimmer der Villa Batarelo'}}

TEMPLATE=r'''<!doctype html>
<html lang="{{lang}}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>{{title}} | Villa Batarelo</title>
<meta name="description" content="{{description}}">
<meta name="theme-color" content="#f5f3ee">
<meta property="og:type" content="website"><meta property="og:title" content="{{title}} | Villa Batarelo"><meta property="og:description" content="{{description}}"><meta property="og:locale" content="{{t.locale}}"><meta property="og:image" content="{{photos[0].src}}">
<meta name="twitter:card" content="summary_large_image">
{% for lg in ['hr','en','de'] %}<link rel="alternate" hreflang="{{lg}}" href="/{{lg}}/{{page if page!='home' else ''}}{% if page!='home' %}/{% endif %}">{% endfor %}
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://static.cupid.travel"><link rel="preconnect" href="https://cf.bstatic.com">
{% if page=='home' %}<link rel="preload" as="image" href="{{photos[0].src}}" fetchpriority="high">{% endif %}
<link rel="stylesheet" href="/assets/css/site.css"><script src="/assets/js/config.js" defer></script><script src="/assets/js/site.js" defer></script>
<script type="application/ld+json">{{schema | safe}}</script>
</head>
<body class="page-{{page}}" data-lang="{{lang}}" data-page="{{page}}">
<a class="skip" href="#main">{{t.nav.home}}</a>
{% if page=='home' %}
<div class="intro" id="intro" aria-hidden="true"><div class="intro-inner"><div class="intro-wordmark">Villa <strong>Batarelo</strong></div></div></div>
{% endif %}
<header class="site-header" id="site-header"><nav class="nav-shell" aria-label="{{t.footer_explore}}">
<a class="brand" href="/{{lang}}/" aria-label="Villa Batarelo"><span class="brand-wordmark">Villa <strong>Batarelo</strong></span></a>
<div class="nav-links" id="nav-links">{% for item in ['home','villa','amenities','gallery','location','contact'] %}<a class="nav-link {% if page==item %}is-current{% endif %}" href="/{{lang}}/{{item if item!='home' else ''}}{% if item!='home' %}/{% endif %}">{{t.nav[item]}}</a>{% endfor %}<div class="nav-mobile-tail"><a href="/{{lang}}/booking/" class="btn btn-dark">{{t.check}}</a></div></div>
<div class="nav-actions"><div class="lang-switch"><button type="button" class="lang-current" aria-expanded="false" aria-label="{{t.lang_switch_label}}">{{lang|upper}}<svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5"/></svg></button><div class="lang-menu">{% for lg in ['hr','en','de'] %}<a {% if lg==lang %}aria-current="true"{% endif %} href="/{{lg}}/{{page if page!='home' else ''}}{% if page!='home' %}/{% endif %}">{{{'hr':'Hrvatski','en':'English','de':'Deutsch'}[lg]}}</a>{% endfor %}</div></div><a class="nav-cta" href="/{{lang}}/booking/">{{t.check}}</a></div>
<button class="mobile-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="{{t.menu_label}}"><span></span><span></span></button>
</nav></header>
<main id="main">
{% if page=='home' %}
<section class="hero hero-home"><img class="hero-image" src="{{photos[0].src}}" data-fallback="{{photos[0].fallback}}" alt="{{alt.exterior}}" fetchpriority="high" decoding="async"><div class="hero-shade"></div><div class="container hero-content"><div class="hero-eyebrow">{{t.eyebrow}}</div><h1>{{t.home_title|safe}}</h1><p>{{t.home_sub}}</p><div class="hero-actions"><a href="/{{lang}}/booking/" class="btn btn-light">{{t.check}}</a><a href="/{{lang}}/villa/" class="text-link light">{{t.explore}}</a></div></div><div class="hero-bottom"><span>{{t.eyebrow}}</span><div class="scroll-cue">{{t.scroll_hint}}</div><span>Lučane · Sinj</span></div></section>
<div class="highlights"><div class="container highlights-grid">{% for stat in t.stats %}<div class="highlight"><span>{{stat}}</span></div>{% endfor %}</div></div>
<section class="section reviews-section"><div class="container"><div class="section-heading center"><span class="kicker">{{t.reviews_k}}</span><h2>{{t.reviews_t|safe}}</h2></div><div class="reviews-grid"><a href="{{booking_url}}" class="rating-card" target="_blank" rel="noopener noreferrer"><span class="rating-source">BOOKING.COM</span><div class="rating-score">10<span>/10</span></div><span class="rating-stars">★★★★★</span><span class="rating-link">{{t.learn}}</span></a><a href="{{airbnb_url}}" class="rating-card" target="_blank" rel="noopener noreferrer"><span class="rating-source">AIRBNB</span><div class="rating-score">4,96<span>/5</span></div><span class="rating-stars">★★★★★</span><span class="rating-link">{{t.learn}}</span></a></div><p class="reviews-note">{{t.review_info}}</p></div></section>
<section class="section section-intro"><div class="container intro-grid"><div class="intro-copy"><span class="kicker">{{t.home_intro_k}}</span><h2>{{t.home_intro_title|safe}}</h2><p class="lead">{{t.home_intro_text}}</p><a class="text-link" href="/{{lang}}/villa/">{{t.learn}}</a></div><div class="intro-visual"><figure class="framed-image tall"><img loading="lazy" src="{{photos[2].src}}" alt="{{alt.bedroom}}"></figure></div></div></section>
<section class="pool-feature"><img loading="lazy" src="{{photos[3].src}}" alt="{{alt.pool}}" class="pool-bg"><div class="pool-overlay"></div><div class="container pool-inner"><div class="pool-text"><span class="kicker kicker-light">{{t.photo_pool_k}}</span><h2>{{t.photo_pool_t|safe}}</h2><p>{{t.photo_pool_p}}</p><a href="/{{lang}}/amenities/" class="btn btn-outline-light">{{t.view_details}}</a></div></div></section>
<section class="section section-amen"><div class="container"><div class="section-heading split"><div><span class="kicker">{{t.main_amen_k}}</span><h2>{{t.main_amen_t|safe}}</h2></div><a class="text-link" href="/{{lang}}/amenities/">{{t.view_details}}</a></div><div class="amen-grid">{% for a in t.amen_short %}<article class="amen-item"><p>{{a}}</p></article>{% endfor %}</div></div></section>
<section class="section gallery-preview"><div class="container"><div class="section-heading center"><span class="kicker">{{t.gallery_k}}</span><h2>{{t.gallery_t|safe}}</h2></div><div class="gallery-feature-grid"><a href="/{{lang}}/gallery/" class="gallery-feature feature-one"><img loading="lazy" src="{{photos[0].src}}" alt="{{alt.exterior}}"><span>{{t.filters.exterior}}</span></a><a href="/{{lang}}/gallery/" class="gallery-feature feature-two"><img loading="lazy" src="{{photos[1].src}}" alt="{{alt.outside}}"><span>{{t.filters.outside}}</span></a><a href="/{{lang}}/gallery/" class="gallery-feature feature-three"><img loading="lazy" src="{{photos[2].src}}" alt="{{alt.bedroom}}"><span>{{t.filters.bedroom}}</span></a></div><div class="centered-action"><a class="btn btn-outline" href="/{{lang}}/gallery/">{{t.see_all}}</a></div></div></section>

<section class="section region-section"><div class="container region-grid"><div class="region-side"><img loading="lazy" src="{{photos[1].src}}" data-fallback="{{photos[1].fallback}}" alt="{{alt.outside}}"><span class="region-label">Villa Batarelo · Lučane</span></div><div><span class="kicker">{{t.location_k}}</span><h2>{{t.location_t|safe}}</h2><p class="lead">{{t.location_p}}</p><a href="/{{lang}}/location/" class="text-link">{{t.learn}}</a></div></div></section>
{% elif page=='villa' %}
{{subhero('villa',t.villa_k,t.villa_title,t.villa_lead,photos[0])|safe}}
<section class="section"><div class="container editorial-grid"><div><span class="kicker">VILLA BATARELO</span><h2>{{t.villa_feature_title|safe}}</h2><p class="lead">{{t.villa_p1}}</p><p>{{t.villa_p2}}</p></div><figure class="editorial-photo"><img loading="lazy" src="{{photos[1].src}}" alt="{{alt.outside}}"></figure></div></section>

<section class="section"><div class="container"><div class="photo-triptych"><img loading="lazy" src="{{photos[2].src}}" alt="{{alt.bedroom}}"><img loading="lazy" src="{{photos[0].src}}" alt="{{alt.exterior}}"><img loading="lazy" src="{{photos[3].src}}" alt="{{alt.pool}}"></div></div></section>
{% elif page=='amenities' %}
{{subhero('amenities',t.amenities_k,t.amenities_title,t.amenities_lead,photos[1])|safe}}
<section class="section"><div class="container"><div class="rooms-grid">{% for name,desc,cat in t.amen_cards %}<article class="room-card"><div class="room-image"><img loading="lazy" src="{{first_photo(cat).src}}" data-fallback="{{first_photo(cat).fallback}}" alt="{{alt[cat]}}"></div><div class="room-body"><h2>{{name}}</h2><p>{{desc}}</p></div></article>{% endfor %}</div></div></section>
<section class="section amen-list-section"><div class="container amen-list-grid"><div><span class="kicker">VILLA BATARELO</span><h2>{{t.amen_list_title}}</h2></div><ul class="amen-list">{% for a in t.amen_list %}<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 12 5 5L20 6"/></svg>{{a}}</li>{% endfor %}</ul></div></section>
{% elif page=='gallery' %}
{{subhero('gallery',t.gallery_page_k,t.gallery_page_t,t.gallery_lead,photos[0])|safe}}
<section class="section gallery-page-content"><div class="container"><div class="filterbar" aria-label="{{t.filter_label}}"><button class="filter-btn is-active" data-filter="all" type="button" aria-pressed="true">{{t.filters.all}}</button>{% for cat in ['exterior','pool','outside','inside','bedroom','bathroom'] %}<button class="filter-btn" data-filter="{{cat}}" type="button" aria-pressed="false">{{t.filters[cat]}}</button>{% endfor %}</div><div class="gallery-masonry" id="photo-gallery">{% for photo in photos %}<button type="button" class="gallery-tile" data-category="{{photo.category}}" data-photo="{{loop.index0}}" aria-label="{{alt[photo.category]}}"><img loading="lazy" src="{{photo.src}}" data-fallback="{{photo.fallback}}" alt="{{alt[photo.category]}}"></button>{% endfor %}</div><div class="gallery-empty" id="gallery-empty" hidden><p>{{t.photo_unavailable}}</p><p><a href="{{booking_url}}" target="_blank" rel="noopener noreferrer">Booking.com</a> · <a href="{{airbnb_url}}" target="_blank" rel="noopener noreferrer">Airbnb</a></p></div></div></section>
<dialog id="lightbox" class="lightbox" aria-label="{{t.lightbox_title}}"><button class="lightbox-close" aria-label="{{t.lightbox_close}}" type="button">×</button><button class="lightbox-prev" aria-label="{{t.lightbox_prev}}" type="button">‹</button><figure><img alt="Villa Batarelo" id="lightbox-image"><figcaption id="lightbox-caption"></figcaption></figure><button class="lightbox-next" aria-label="{{t.lightbox_next}}" type="button">›</button></dialog>
{% elif page=='location' %}
{{subhero('location',t.location_page_k,t.location_page_t,t.location_lead,photos[0])|safe}}
<section class="section"><div class="container"><div class="places-grid">{% for name,desc,query in t.places %}<article class="place-card"><h2>{{name}}</h2><p>{{desc}}</p><a href="https://www.google.com/maps/search/?api=1&amp;query={{query|urlencode}}" target="_blank" rel="noopener noreferrer" class="place-map-link">{{t.place_action}}</a></article>{% endfor %}</div></div></section>
<section class="section map-section"><div class="container map-grid"><div><span class="kicker">LUČANE · SINJ</span><h2>{{t.map_title}}</h2><p>{{t.map_note}}</p><a target="_blank" rel="noopener noreferrer" class="btn btn-dark" href="https://www.google.com/maps/search/?api=1&amp;query=Lu%C4%8Dane+33c+21230+Sinj+Croatia">{{t.map_button}}</a></div><div class="map-real" id="map-real"><div class="map-optin"><span class="map-optin-name">Villa Batarelo</span><p>Lučane 33c · 21230 Sinj</p><p class="map-optin-notice">{{t.map_notice}}</p><button type="button" class="btn btn-dark map-activate" data-map-load="true">{{t.map_load}}</button></div></div></div></section>
{% elif page=='booking' %}
{{subhero('booking',t.booking_page_k,t.booking_page_t,t.booking_lead,photos[1])|safe}}
<section class="section booking-section"><div class="container booking-grid"><div class="booking-info"><h2>{{t.booking_info_title}}</h2><div class="contact-short"><span>{{t.wa}} / {{t.call}}</span><a href="tel:+385955846044">+385 95 584 6044</a></div><div class="contact-short"><span>{{t.footer_email}}</span><a href="mailto:davorbatarelo1961@gmail.com">davorbatarelo1961@gmail.com</a></div><p class="muted-small">{{t.form_note}}</p></div><div class="booking-form-card">{{form(t)|safe}}</div></div></section>
<section class="platform-section"><div class="container platform-row"><span>{{t.platforms}}</span><a href="{{booking_url}}" target="_blank" rel="noopener noreferrer">Booking.com</a><a href="{{airbnb_url}}" target="_blank" rel="noopener noreferrer">Airbnb</a></div></section>
{% elif page=='contact' %}
{{subhero('contact',t.contact_k,t.contact_title,t.contact_lead,photos[2])|safe}}
<section class="section"><div class="container contact-cards"><a href="tel:+385955846044" class="contact-card"><span class="kicker">{{t.call}}</span><strong>+385 95 584 6044</strong></a><a href="https://wa.me/385955846044" target="_blank" rel="noopener noreferrer" class="contact-card"><span class="kicker">WhatsApp</span><strong>{{t.wa}}</strong></a><a href="mailto:davorbatarelo1961@gmail.com" class="contact-card"><span class="kicker">{{t.footer_email}}</span><strong class="mail-contact">davorbatarelo1961@gmail.com</strong></a></div></section>
<section class="section contact-faq"><div class="container faq-grid"><div><span class="kicker">{{t.questions}}</span><h2>{{t.faq_t}}</h2></div><div class="faq-list">{% for question,answer in t.faq %}<details><summary>{{question}}<span aria-hidden="true">+</span></summary><p>{{answer}}</p></details>{% endfor %}</div></div></section>
{% else %}
<section class="legal-top"><div class="container"><span class="kicker">VILLA BATARELO</span><h1>{{t[page+'_title']}}</h1><p>{{t.legal_notice}}</p></div></section><section class="section legal-content"><div class="container prose">{% for paragraph in t[page+'_body'] %}<p>{{paragraph}}</p>{% endfor %}<p><a href="mailto:davorbatarelo1961@gmail.com">davorbatarelo1961@gmail.com</a> · <a href="tel:+385955846044">+385 95 584 6044</a></p></div></section>
{% endif %}
{% if page in ['home','gallery','location'] %}<section class="booking-cta"><div class="container booking-cta-grid"><div><h2>{{t.booking_banner_t|safe}}</h2><p>{{t.booking_banner_p}}</p></div><a class="btn btn-light" href="/{{lang}}/booking/">{{t.cta}}</a></div></section>{% endif %}
</main>
<footer class="footer"><div class="container"><div class="footer-top"><div class="footer-brand"><a class="brand brand-footer" href="/{{lang}}/"><span class="brand-wordmark">Villa <strong>Batarelo</strong></span></a><p>{{t.tagline}}</p></div><div><span class="footer-label">{{t.footer_explore}}</span>{% for item in ['villa','amenities','gallery','location'] %}<a href="/{{lang}}/{{item}}/">{{t.nav[item]}}</a>{% endfor %}</div><div><span class="footer-label">{{t.footer_contact}}</span><a href="tel:+385955846044">+385 95 584 6044</a><a href="mailto:davorbatarelo1961@gmail.com">{{t.footer_email}}</a><a href="https://wa.me/385955846044" target="_blank" rel="noopener noreferrer">WhatsApp</a><span>Lučane 33c, Sinj</span></div><div><span class="footer-label">{{t.footer_bookings}}</span><a href="/{{lang}}/booking/">{{t.check}}</a><a href="{{booking_url}}" target="_blank" rel="noopener noreferrer">Booking.com</a><a href="{{airbnb_url}}" target="_blank" rel="noopener noreferrer">Airbnb</a></div></div><div class="footer-bottom"><span>© <span id="year">2026</span> Villa Batarelo. {{t.copyright}}</span><div class="footer-legals">{% for item in ['privacy','cookies','terms'] %}<a href="/{{lang}}/{{item}}/">{{t.nav[item]}}</a>{% endfor %}<button type="button" class="cookie-open">{{t.cookie_settings}}</button></div><span>{{t.built}}</span></div></div></footer>
<div class="floating-actions"><a class="floating-phone" href="tel:+385955846044" aria-label="{{t.call}}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 3h5l2 5-3 2c1.5 3 3 4.5 6 6l2-3 5 2v5c-8.5 1-18-8.5-17-17Z"/></svg></a><a class="floating-wa" target="_blank" rel="noopener noreferrer" href="https://wa.me/385955846044" aria-label="{{t.wa}}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.9a8.5 8.5 0 0 1-12.6 7.5L3 21l1.6-4.8A8.5 8.5 0 1 1 20.5 12Z"/><path d="M8.4 8.1c-.5.7-.3 1.7.2 2.7.9 1.9 2.3 3.3 4.2 4.1 1.1.5 2 .6 2.7 0l-1.9-1.4-1.2 1c-1.4-.8-2.4-1.9-3.1-3.1l.9-1.3Z"/></svg></a></div>
<div class="cookie-banner" id="cookie-banner" role="dialog" aria-label="{{t.cookie_settings}}"><div><strong>{{t.cookie_settings}}</strong><p>{{t.cookie_notice}}</p></div><div class="cookie-actions"><button type="button" data-cookie="reject">{{t.reject}}</button><button class="cookie-accept" type="button" data-cookie="accept">{{t.accept}}</button></div></div>
</body></html>'''

def subhero(page,k,title,lead,photo):
 return f'''<section class="subhero subhero-{page}"><img class="subhero-img" src="{escape(photo['src'],quote=True)}" data-fallback="{escape(photo['fallback'],quote=True)}" alt="Villa Batarelo" fetchpriority="high"><div class="subhero-shade"></div><div class="container subhero-content"><span class="kicker kicker-light">{escape(k)}</span><h1>{title}</h1><p>{escape(lead)}</p></div><div class="subhero-count">VILLA BATARELO · SINJ</div></section>'''

def form(t):
 def field(id,label,typ='text',required=False,extra=''):
  return f'<div class="form-field"><label for="{id}">{escape(label)}</label><input id="{id}" name="{id}" type="{typ}" {"required" if required else ""} {extra}></div>'
 html=f'<form id="enquiry-form" novalidate><h2>{escape(t["form_title"])}</h2><div class="form-grid">'
 html+=field('arrival',t['arrival'],'date',True)+field('departure',t['departure'],'date',True)
 html+=f'<div class="form-field"><label for="guests">{escape(t["guests"])}</label><select id="guests" name="guests" required>'+''.join(f'<option value="{i}">{i}</option>' for i in range(1,7))+'</select></div>'
 html+=field('name',t['name'],'text',True,'autocomplete="name" minlength="2"')
 html+=field('email',t['email'],'email',True,'autocomplete="email"')
 html+=field('phone',t['phone'],'tel',False,'autocomplete="tel"')
 html+=f'</div><div class="form-field"><label for="message">{escape(t["message"])}</label><textarea id="message" name="message" rows="4" maxlength="1500"></textarea></div>'
 html+=f'<label class="form-consent"><input id="consent" name="consent" type="checkbox" required><span>{escape(t["consent"])}</span></label><p class="form-error" id="form-error" role="alert" hidden>{escape(t["validation"])}</p>'
 html+=f'<button type="submit" class="btn btn-dark form-submit">{escape(t["send"])}</button><a href="mailto:davorbatarelo1961@gmail.com" class="email-form-link" id="email-form-link">{escape(t["email_option"])}</a><p class="form-note">{escape(t["sent_note"])}</p></form>'
 return html


def first_photo(cat):
 for p in photos:
  if p['category']==cat:return p
 return photos[0]

def schema_json(lang,page):
 o={'@context':'https://schema.org','@type':'LodgingBusiness','name':'Villa Batarelo','description':LANGS[lang]['home_sub'],'telephone':'+385955846044','email':'davorbatarelo1961@gmail.com','address':{'@type':'PostalAddress','streetAddress':'Lučane 33c','postalCode':'21230','addressLocality':'Sinj','addressCountry':'HR'},'image':FALLBACKS,'sameAs':[BOOKING,AIRBNB],'amenityFeature':[{'@type':'LocationFeatureSpecification','name':v,'value':True} for v in ['Private pool','Wi-Fi','Air conditioning','Free parking']]}
 return json.dumps(o,ensure_ascii=False)

env=Environment(loader=BaseLoader(),autoescape=True,trim_blocks=True,lstrip_blocks=True)
tmpl=env.from_string(TEMPLATE)
for lang,t in LANGS.items():
 for page in PAGES:
  title=t['nav'][page] if page!='home' else {'hr':'Privatna vila s bazenom u Sinju','en':'Private Pool Villa near Sinj','de':'Private Villa mit Pool bei Sinj'}[lang]
  desc=t.get({'privacy':'meta_privacy','cookies':'meta_cookies','terms':'meta_terms','home':'home_sub','villa':'villa_lead','amenities':'amenities_lead','gallery':'gallery_lead','location':'location_lead','booking':'booking_lead','contact':'contact_lead'}.get(page,'legal_notice'),t['legal_notice'])
  outdir=ROOT/lang/(page if page!='home' else '')
  outdir.mkdir(parents=True,exist_ok=True)
  rendered=tmpl.render(lang=lang,t=t,page=page,title=title,description=desc,photos=photos,alt=PICALT[lang],subhero=subhero,first_photo=first_photo,form=form,schema=schema_json(lang,page),booking_url=BOOKING,airbnb_url=AIRBNB)
  (outdir/'index.html').write_text(rendered,encoding='utf8')
(ROOT/'index.html').write_text('<!doctype html><html lang="hr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/hr/"><script>location.replace("/hr/")</script><title>Villa Batarelo</title></head><body><a href="/hr/">Villa Batarelo</a></body></html>',encoding='utf8')
# Source manifest to simplify switching to local owner assets later.
manifest={'important':'Property gallery photographs are still remote, not bundled or converted. Remote URLs can fail; failed gallery tiles are hidden rather than replaced with unrelated photos. Owner approval and originals are required before public release.','verified_originals':FALLBACKS,'booking_cdn_photos':_original_photos[4:]}
(ROOT/'assets'/'img'/'photo-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
print('Generated',len(LANGS)*len(PAGES)+1,'HTML pages. Remote property images:',len(photos))
