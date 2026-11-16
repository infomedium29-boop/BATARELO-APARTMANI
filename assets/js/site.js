'use strict';
(() => {
 const doc=document, body=doc.body, lang=body.dataset.lang||'hr', conf=window.VILLA_CONFIG||{};
 const copy={
 hr:{label:'Upit za Villu Batarelo',arrival:'Dolazak',departure:'Odlazak',guests:'Gosti',name:'Ime',email:'E-mail',phone:'Telefon',message:'Poruka',privacy:'Privola za odgovor na upit',img:'Fotografija'},
 en:{label:'Villa Batarelo enquiry',arrival:'Check-in',departure:'Check-out',guests:'Guests',name:'Name',email:'Email',phone:'Phone',message:'Message',privacy:'Consent to reply to this enquiry',img:'Photograph'},
 de:{label:'Anfrage Villa Batarelo',arrival:'Anreise',departure:'Abreise',guests:'Gäste',name:'Name',email:'E-Mail',phone:'Telefon',message:'Nachricht',privacy:'Einwilligung für die Beantwortung',img:'Foto'}
 }[lang];
 const qs=(s,root=doc)=>root.querySelector(s), qsa=(s,root=doc)=>Array.from(root.querySelectorAll(s));
 // Gallery tiles disappear if their remote images fail, instead of repeating an unrelated room or pool photo.
 qsa('img[data-fallback]').forEach(img=>{img.addEventListener('error',()=>{
  const tile=img.closest('.gallery-tile');
  if(tile){tile.dataset.failed='true';tile.hidden=true;doc.dispatchEvent(new CustomEvent('villa-gallery-image-failed'));return;}
  const attempt=Number(img.dataset.fallbackAttempt||0);
  if(attempt===0&&img.dataset.fallback&&img.src!==img.dataset.fallback){img.dataset.fallbackAttempt='1';img.src=img.dataset.fallback;}
  else if(attempt<2){img.dataset.fallbackAttempt='2';img.src='/assets/img/photo-pending.svg';}
 });});
 // Header / menu.
 const header=qs('#site-header');let lastScroll=0;
 const updateHeader=()=>{if(header)header.classList.toggle('scrolled',window.scrollY>45);lastScroll=window.scrollY;};
 updateHeader();addEventListener('scroll',updateHeader,{passive:true});
 const toggle=qs('.mobile-toggle'),menu=qs('.nav-links');
 const closeMenu=()=>{if(!toggle)return;toggle.setAttribute('aria-expanded','false');body.classList.remove('menu-open');};
 toggle?.addEventListener('click',()=>{let open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));body.classList.toggle('menu-open',open);});
 qsa('.nav-link,.nav-mobile-tail a').forEach(a=>a.addEventListener('click',closeMenu));
 // Language control.
 const langs=qs('.lang-switch'),langButton=qs('.lang-current');
 langButton?.addEventListener('click',()=>{const opening=!langs.classList.contains('is-open');langs.classList.toggle('is-open',opening);langButton.setAttribute('aria-expanded',String(opening));});
 doc.addEventListener('click',e=>{if(langs&&!langs.contains(e.target)){langs.classList.remove('is-open');langButton?.setAttribute('aria-expanded','false');}if(body.classList.contains('menu-open')&&header&&!header.contains(e.target))closeMenu();if(e.target===menu)closeMenu();});
 addEventListener('resize',()=>{if(innerWidth>980)closeMenu();},{passive:true});
 doc.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();langs?.classList.remove('is-open');}});
 // Intro only once per browser tab session.
 const intro=qs('#intro');if(intro){let seen=false;try{seen=sessionStorage.getItem('vb-intro-seen')==='1';sessionStorage.setItem('vb-intro-seen','1');}catch{}
 if(seen||matchMedia('(prefers-reduced-motion: reduce)').matches){intro.remove();}else{setTimeout(()=>{intro.classList.add('is-leaving');setTimeout(()=>intro.remove(),710)},1670);}}
 // Gallery categories + accessible lightbox with keyboard controls and touch swipes.
 const gallery=qs('#photo-gallery'),dialog=qs('#lightbox');
 if(gallery&&dialog){let visible=[],index=0,xStart=0;
 const tiles=qsa('.gallery-tile',gallery),lightImg=qs('#lightbox-image'),cap=qs('#lightbox-caption');
 const resetVisible=()=>{visible=tiles.filter(t=>!t.hidden && t.dataset.failed!=='true');const empty=qs('#gallery-empty');if(empty)empty.hidden=visible.length>0;};resetVisible();doc.addEventListener('villa-gallery-image-failed',resetVisible);
 qsa('.filter-btn').forEach(btn=>btn.addEventListener('click',()=>{
  const filter=btn.dataset.filter;qsa('.filter-btn').forEach(b=>{b.classList.toggle('is-active',b===btn);b.setAttribute('aria-pressed',String(b===btn));});
  tiles.forEach(t=>{t.hidden=t.dataset.failed==='true'||(filter!=='all'&&t.dataset.category!==filter);});resetVisible();
 }));
 const show=(i)=>{if(!visible.length)return;index=(i+visible.length)%visible.length;const source=qs('img',visible[index]);lightImg.src=source.currentSrc||source.src;lightImg.alt=source.alt;lightImg.dataset.fallback='/assets/img/photo-pending.svg';cap.textContent=`${copy.img} ${index+1} / ${visible.length}`;};
 const open=tile=>{resetVisible();if(visible.indexOf(tile)<0)return;show(visible.indexOf(tile));dialog.showModal();body.classList.add('modal-open');};
 tiles.forEach(tile=>tile.addEventListener('click',()=>open(tile)));
 qs('.lightbox-close')?.addEventListener('click',()=>dialog.close());qs('.lightbox-prev')?.addEventListener('click',()=>show(index-1));qs('.lightbox-next')?.addEventListener('click',()=>show(index+1));
 dialog.addEventListener('close',()=>{body.classList.remove('modal-open');lightImg.removeAttribute('src');});
 dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
 doc.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='ArrowRight')show(index+1);if(e.key==='ArrowLeft')show(index-1);});
 dialog.addEventListener('touchstart',e=>{xStart=e.changedTouches[0].screenX;},{passive:true});dialog.addEventListener('touchend',e=>{const d=e.changedTouches[0].screenX-xStart;if(Math.abs(d)>55)show(index+(d<0?1:-1));},{passive:true});
 }
 // Reservation enquiry is explicitly non-binding. Frontend works without an API key via WhatsApp / email.
 const form=qs('#enquiry-form');if(form){
  const arrival=qs('#arrival'),departure=qs('#departure'),emailLink=qs('#email-form-link'),error=qs('#form-error');
  const today=new Date();const iso=new Date(today.getTime()-today.getTimezoneOffset()*60000).toISOString().slice(0,10);
  arrival.min=iso;departure.min=iso;
  // Use the original native date picker, but present its value inside a
  // fixed-size visual control so iPhone Safari cannot widen the form field.
  const dateLocale={hr:'hr-HR',en:'en-GB',de:'de-DE'}[lang]||'hr-HR';
  const updateDateDisplay=(input)=>{
    const display=qs('#'+input.id+'-display');
    if(!display)return;
    if(input.value){
      const [year,month,day]=input.value.split('-').map(Number);
      display.textContent=new Date(year,month-1,day).toLocaleDateString(dateLocale,{day:'2-digit',month:'2-digit',year:'numeric'});
      display.classList.remove('is-placeholder');
    }else{
      display.textContent={hr:'Odaberite datum',en:'Select date',de:'Datum auswählen'}[lang]||'Odaberite datum';
      display.classList.add('is-placeholder');
    }
  };
  [arrival,departure].forEach(input=>{
    updateDateDisplay(input);
    input.addEventListener('change',()=>updateDateDisplay(input));
    input.addEventListener('input',()=>updateDateDisplay(input));
  });
  arrival.addEventListener('change',()=>{
    departure.min=arrival.value||iso;
    if(departure.value&&departure.value<=arrival.value){departure.value='';updateDateDisplay(departure);}
  });
  const check=()=>{const a=arrival.value,b=departure.value;let valid=form.checkValidity()&&a>=iso&&b>a;if(!valid){error.hidden=false;form.reportValidity();}else error.hidden=true;return valid;};
  const message=()=>{const data=new FormData(form);const f=key=>String(data.get(key)||'').trim();return `${copy.label}\n\n${copy.arrival}: ${f('arrival')}\n${copy.departure}: ${f('departure')}\n${copy.guests}: ${f('guests')}\n${copy.name}: ${f('name')}\n${copy.email}: ${f('email')}\n${copy.phone}: ${f('phone')||'-'}\n${copy.message}: ${f('message')||'-'}\n\n${copy.privacy}: yes`;};
  form.addEventListener('submit',e=>{e.preventDefault();if(!check())return;const url='https://wa.me/'+(conf.whatsapp||'385955846044')+'?text='+encodeURIComponent(message());const win=window.open(url,'_blank','noopener,noreferrer');if(!win)window.location.href=url;});
  emailLink?.addEventListener('click',e=>{e.preventDefault();if(!check())return;window.location.href=`mailto:${conf.email||'davorbatarelo1961@gmail.com'}?subject=${encodeURIComponent(copy.label)}&body=${encodeURIComponent(message())}`;});
 }
 // Consent; optional analytics remains disabled by default.
 const banner=qs('#cookie-banner'),consentKey='villa-batarelo-cookie-consent';
 let choice=null;try{choice=localStorage.getItem(consentKey)}catch{}
 const setConsent=val=>{try{localStorage.setItem(consentKey,val)}catch{}banner?.classList.remove('is-visible');if(val==='accept')loadAnalytics();};
 function loadAnalytics(){const id=(conf.ga4MeasurementId||'').trim();if(!id||!/^G-[A-Z0-9]+$/.test(id)||window.__vbAnalyticsLoaded)return;window.__vbAnalyticsLoaded=true;const script=doc.createElement('script');script.async=true;script.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id)}`;doc.head.appendChild(script);window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};window.gtag('js',new Date());window.gtag('config',id,{anonymize_ip:true});}
 if(choice===null)banner?.classList.add('is-visible');if(choice==='accept')loadAnalytics();
 qsa('[data-cookie]').forEach(btn=>btn.addEventListener('click',()=>setConsent(btn.dataset.cookie)));
 qsa('.cookie-open').forEach(btn=>btn.addEventListener('click',()=>banner?.classList.add('is-visible')));
 const year=qs('#year');if(year)year.textContent=new Date().getFullYear().toString();
})();
