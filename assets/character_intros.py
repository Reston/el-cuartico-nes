"""Original two-page NES posters for Chuchito and The Lion Queen."""
from PIL import Image, ImageDraw
from likeness import menu_portrait

PALETTES = [
    bytes([0x0f,0x07,0x17,0x27, 0x0f,0x07,0x27,0x30,
           0x0f,0x0f,0x27,0x37, 0x0f,0x0f,0x1b,0x2b]),
    bytes([0x0f,0x07,0x17,0x27, 0x0f,0x07,0x27,0x30,
           0x0f,0x0f,0x27,0x37, 0x0f,0x06,0x16,0x26]),
]

def build_card(root,font,pack,host,first_bank):
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    def caption(label,y,scale=1,ink=3):
        x=(256-(len(label)*6-1)*scale)//2
        for ch in label:
            glyph=font.get('A' if ch=='Á' else ch,['00000']*7)
            for gy,row in enumerate(glyph):
                for gx,v in enumerate(row):
                    if v=='1':d.rectangle((x+gx*scale,y+gy*scale,x+(gx+1)*scale-1,y+(gy+1)*scale-1),fill=ink)
            if ch=='Á':d.line((x+2*scale,y-3,x+4*scale,y-5),fill=ink,width=scale)
            x+=6*scale
    d.rectangle((8,8,247,231),outline=2,width=2)
    d.rectangle((12,12,243,227),outline=1)
    for x in (18,234):
        for y in (18,216):d.polygon([(x,y),(x+3,y+3),(x,y+6),(x-3,y+3)],fill=3)
    if host==0:
        # Warm acoustic walls, stage bulbs and a hand-painted studio marquee.
        for x in range(24,240,8):
            d.line((x,24,x,39),fill=1)
            d.line((x,99,x,207),fill=1)
        d.rectangle((20,44,235,92),fill=1,outline=3,width=2)
        d.line((24,48,231,48),fill=2)
        caption('CHUCHITO',53,3)
        caption('EL RUFIÁN',80,1)
        caption('UNA TOMA. DOCE REPARACIONES.',24,1,2)
        for x in (27,224):
            for y in range(112,184,16):d.ellipse((x,y,x+4,y+4),fill=3)
        # Cables, mixer and camera frame the familiar green-shirted host.
        d.rounded_rectangle((39,153,77,185),radius=3,fill=1,outline=2)
        for x in (46,57,68):
            d.line((x,160,x,179),fill=3)
            d.rectangle((x-2,164+(x%3)*3,x+2,167+(x%3)*3),fill=2)
        d.line((53,186,53,198,77,198,84,191),fill=2,width=2)
        d.rectangle((180,130,209,151),fill=1,outline=3)
        d.polygon([(209,137),(219,132),(219,151),(209,146)],fill=2)
        d.ellipse((181,117,194,130),fill=2,outline=3)
        d.ellipse((196,117,209,130),fill=2,outline=3)
        d.line((194,152,194,180),fill=2,width=2)
        d.line((194,169,182,190),fill=2,width=2);d.line((194,169,206,190),fill=2,width=2)
        portrait=menu_portrait(0,gear=False)
        im.paste(portrait,(96,128))
        d.line((88,192,167,192),fill=2,width=2)
        caption('QUE NO SE CAIGA EL PROGRAMA',203,1,2)
    else:
        # A theatre sunrise, velvet curtains and a crown above Estefania.
        d.ellipse((69,82,187,200),fill=2)
        for y in range(145,202,8):d.line((66,y,190,y),fill=1)
        for x in (16,208):
            d.polygon([(x,18),(x+31,18),(x+31,95),(x+19,145),(x,180)],fill=1)
            for dx in (4,12,20):d.line((x+dx,20,x+dx,114-dx),fill=2)
        d.polygon([(28,188),(88,173),(110,181),(174,175),(229,205),(229,214),(28,214)],fill=1)
        d.polygon([(71,193),(97,186),(119,189),(149,183),(180,199)],fill=3)
        d.polygon([(95,198),(115,192),(146,192),(156,212),(103,212)],fill=2)
        caption('THE',25,2)
        caption('LION QUEEN',49,3)
        caption('ESTEFANIA',80,1,3)
        im.paste(menu_portrait(1,gear=False),(96,128))
        d.polygon([(115,122),(112,112),(120,117),(127,106),(134,117),(142,112),(139,123)],fill=3,outline=1)
        d.rectangle((115,123,139,126),fill=2)
        for x,y in ((77,106),(179,111),(63,130),(197,136)):
            d.line((x-3,y,x+3,y),fill=3);d.line((x,y-3,x,y+3),fill=3)
        caption('EL ESCENARIO ES TUYO',203,1,3)
    d.rectangle((24,216,231,225),fill=0)
    caption('A / START: COMENZAR',218,1,3)
    # Character skins, costume and backdrop get independent 8x8 palettes.
    def palette(x,y):
        if 96<=x<160 and 128<=y<176:return 2
        if 96<=x<160 and 176<=y<192:return 3 if host==0 else 0
        if y<96 or y>=216:return 1
        return 0 if host==0 or 64<=x<192 else 3
    tiles=[];ids=[];attrs=[]
    for y in range(0,240,8):
        for x in range(0,256,8):
            tile=pack(im.crop((x,y,x+8,y+8)))
            if tile not in tiles:tiles.append(tile)
            n=tiles.index(tile);ids.append(n&255);attrs.append((palette(x,y)<<6)|first_bank+n//256)
    assert len(tiles)<=512,('character intro',host,len(tiles))
    stem=('chucho','estefania')[host]+'-intro'
    root.joinpath(stem+'.nam').write_bytes(bytes(ids)+bytes(64))
    root.joinpath(stem+'.exram').write_bytes(bytes(attrs)+bytes(64))
    root.joinpath(stem+'.pal').write_bytes(PALETTES[host])
    return b''.join(tiles)+bytes((512-len(tiles))*16),len(tiles)
