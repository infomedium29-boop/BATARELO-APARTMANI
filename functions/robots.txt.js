export function onRequestGet({request}){return new Response(`User-agent: *\nAllow: /\nSitemap: ${new URL(request.url).origin}/sitemap.xml\n`,{headers:{'content-type':'text/plain;charset=utf-8'}})}
