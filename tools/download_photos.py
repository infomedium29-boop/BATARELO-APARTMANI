#!/usr/bin/env python3
"""
Optional owner-approved photo downloader for Villa Batarelo.
Downloads only public image URLs already in assets/img/photo-manifest.json.
No logins, circumvention, scraping protected pages or mass discovery.
Usage: pip install requests pillow pillow-avif-plugin
       python tools/download_photos.py
"""
from pathlib import Path
from io import BytesIO
import sys,json
try:
 import requests
 from PIL import Image
except ImportError:
 print('Install dependencies: pip install requests pillow pillow-avif-plugin');sys.exit(1)
try:import pillow_avif
except ImportError:pass
R=Path(__file__).resolve().parents[1]; dest=R/'assets'/'img'/'villa';dest.mkdir(exist_ok=True)
manifest=json.loads((R/'assets'/'img'/'photo-manifest.json').read_text(encoding='utf8'))
images=[{'id':'cover','src':manifest['verified_originals'][0]}, {'id':'terrace','src':manifest['verified_originals'][1]}, {'id':'bedroom-main','src':manifest['verified_originals'][3]}, {'id':'pool-evening','src':manifest['verified_originals'][2]}]+manifest['booking_cdn_photos']
results={};failed=[];success=[]
session=requests.Session();session.headers.update({'User-Agent':'Mozilla/5.0 (compatible; VillaBatareloAssetImport/1.0)'})
for i,p in enumerate(images,1):
 pid=p['id'];url=p['src'];print(f'[{i}/{len(images)}] {pid} ...',end=' ',flush=True)
 try:
  response=session.get(url,timeout=20,allow_redirects=True);response.raise_for_status()
  if not response.headers.get('content-type','').startswith('image/'):raise ValueError('not an image')
  if len(response.content)<8000:raise ValueError('image too small')
  image=Image.open(BytesIO(response.content));image.load()
  if image.width<480 or image.height<330:raise ValueError('low-resolution image')
  if image.mode not in ['RGB','RGBA']:image=image.convert('RGB')
  if image.mode=='RGBA':image=image.convert('RGB')
  image.thumbnail((1800,1600))
  webp=dest/f'{pid}.webp';image.save(webp,'WEBP',quality=83,method=5)
  try:
   avif=dest/f'{pid}.avif';image.save(avif,'AVIF',quality=58)
   src=f'/assets/img/villa/{pid}.avif'
  except Exception:
   src=f'/assets/img/villa/{pid}.webp'
  results[pid]={'src':src,'fallback':f'/assets/img/villa/{pid}.webp'}
  success.append(pid)
  print('OK')
 except Exception as exc:
  failed.append({'id':pid,'reason':str(exc)[:180]});print('SKIPPED:',str(exc)[:90])
(R/'assets'/'img'/'photo-map.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
(R/'assets'/'img'/'photo-import-report.json').write_text(json.dumps({'success':success,'failed':failed},ensure_ascii=False,indent=2),encoding='utf8')
print(f'Imported {len(success)} / {len(images)} images. Build site with: python tools/build_site.py')
