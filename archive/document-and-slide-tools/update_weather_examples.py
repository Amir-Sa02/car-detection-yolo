from __future__ import annotations

import copy
import io
import zipfile
from datetime import datetime
from pathlib import Path

from lxml import etree
from PIL import Image

ROOT = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی')
PPT = ROOT/'documents'/'ارائه_دفاع_نهایی_جلسه.pptx'
ASSET = ROOT/'figures and plots'/'چهار_وضعیت_هرکدام_یک_نمونه.png'
BACKUP = ROOT/'documents'/'پشتیبان‌ها'/('ارائه_دفاع_نهایی_جلسه_پیش_از_اصلاح_نمونه‌ها_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.pptx')

NS = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'pr':'http://schemas.openxmlformats.org/package/2006/relationships'}
EMU = 914400

def build_asset(img_left: Image.Image, img_right: Image.Image):
    # Source figures are arranged: Day A/B, Night A/B and Rain A/B, Cloud A/B.
    # Select the FIRST row of each condition. No crop touches the frame itself.
    assert img_left.size == img_right.size == (2101,2477)
    w,h=4202,1748
    canvas=Image.new('RGB',(w,h),'white')
    y0=195
    # The final 91 px of each source contains rotated row labels. They are
    # clipped at slide scale, while the slide already captions each group.
    for x,img in ((46,img_left),(2146,img_right)):
        canvas.paste(img.crop((0,0,2010,68)),(x,y0))
        canvas.paste(img.crop((0,68,2010,630)),(x,y0+68))
        canvas.paste(img.crop((0,1251,2010,1813)),(x,y0+68+562+42))
    # One shared class legend, taken from the original figure.
    canvas.paste(img_left.crop((0,2385,2101,2477)),(1050,1490))
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(ASSET,optimize=True)
    return ASSET.read_bytes()

def main():
    with zipfile.ZipFile(PPT,'r') as source:
        slide_name='ppt/slides/slide27.xml'
        rels_name='ppt/slides/_rels/slide27.xml.rels'
        slide=etree.fromstring(source.read(slide_name))
        rels=etree.fromstring(source.read(rels_name))
        pics=slide.xpath('.//p:spTree/p:pic',namespaces=NS)
        assert len(pics)==3, f'Expected 3 pictures including logo, got {len(pics)}'
        shape_tree=slide.xpath('.//p:spTree',namespaces=NS)[0]
        source_blobs=[]
        for pic in pics[:2]:
            rid=pic.xpath('.//a:blip',namespaces=NS)[0].get('{'+NS['r']+'}embed')
            rel=rels.xpath('./pr:Relationship[@Id="'+rid+'"]',namespaces=NS)[0]
            media=rel.get('Target').split('/')[-1]
            source_blobs.append(source.read('ppt/media/'+media))
        image_data=build_asset(*(Image.open(io.BytesIO(b)).convert('RGB') for b in source_blobs))
        first,second=pics[:2]
        new_rid='rIdWeatherSingle'
        assert not rels.xpath('./pr:Relationship[@Id="'+new_rid+'"]',namespaces=NS)
        rel=etree.SubElement(rels,'{'+NS['pr']+'}Relationship')
        rel.set('Id',new_rid)
        rel.set('Type','http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
        rel.set('Target','../media/weather_single_each.png')
        first.xpath('.//a:blip',namespaces=NS)[0].set('{'+NS['r']+'}embed',new_rid)
        xfrm=first.xpath('./p:spPr/a:xfrm',namespaces=NS)[0]
        xfrm.xpath('./a:off',namespaces=NS)[0].attrib.update({'x':str(round(.45*EMU)),'y':str(round(1.27*EMU))})
        xfrm.xpath('./a:ext',namespaces=NS)[0].attrib.update({'cx':str(round(12.43*EMU)),'cy':str(round(5.17*EMU))})
        shape_tree.remove(second)
        backup_data=PPT.read_bytes()
        BACKUP.parent.mkdir(parents=True,exist_ok=True)
        BACKUP.write_bytes(backup_data)
        tmp=PPT.with_suffix('.tmp.pptx')
        with zipfile.ZipFile(tmp,'w') as dest:
            for item in source.infolist():
                data=source.read(item.filename)
                if item.filename==slide_name: data=etree.tostring(slide,encoding='UTF-8',xml_declaration=True,standalone=True)
                elif item.filename==rels_name: data=etree.tostring(rels,encoding='UTF-8',xml_declaration=True,standalone=True)
                dest.writestr(item,data)
            dest.writestr('ppt/media/weather_single_each.png',image_data,compress_type=zipfile.ZIP_DEFLATED)
    tmp.replace(PPT)
    print('backup',BACKUP)
    print('asset',ASSET)
    print('updated',PPT)

if __name__=='__main__': main()
