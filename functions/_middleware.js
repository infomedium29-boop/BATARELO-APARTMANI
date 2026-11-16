/**
 * Cloudflare Pages middleware injects correct absolute canonical + hreflang URLs
 * on the deployed domain without baking a fake domain into the ZIP.
 */
export async function onRequest(context){
  const response = await context.next();
  const contentType=response.headers.get('content-type')||'';
  if(!contentType.includes('text/html')||response.status!==200)return response;
  const url=new URL(context.request.url);
  let html=await response.text();
  html=html.replace(/<link rel="alternate" hreflang="(hr|en|de)" href="(\/[^\"]+)">/g,
    (_,locale,path)=>`<link rel="alternate" hreflang="${locale}" href="${url.origin}${path}">`);
  html=html.replace('</head>',`<link rel="canonical" href="${url.origin}${url.pathname}"><meta property="og:url" content="${url.origin}${url.pathname}"></head>`);
  const headers=new Headers(response.headers);headers.delete('content-length');
  return new Response(html,{status:response.status,statusText:response.statusText,headers});
}
