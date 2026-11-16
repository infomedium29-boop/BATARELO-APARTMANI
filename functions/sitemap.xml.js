export function onRequestGet({request}) {
 const base = new URL(request.url).origin;
 const pages = ['','villa/','amenities/','gallery/','location/','booking/','contact/','privacy/','cookies/','terms/'];
 const langs = ['hr','en','de'];
 const esc=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;');
 const body = pages.map(page=>langs.map(l=>`<url><loc>${esc(base)}/${l}/${page}</loc>${langs.map(alt=>`<xhtml:link rel="alternate" hreflang="${alt}" href="${esc(base)}/${alt}/${page}"/>`).join('')}<changefreq>${page?'monthly':'weekly'}</changefreq><priority>${page?'.7':'1.0'}</priority></url>`).join('')).join('');
 return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${body}</urlset>`,{headers:{'content-type':'application/xml;charset=utf-8','cache-control':'public, max-age=3600'}});
}
