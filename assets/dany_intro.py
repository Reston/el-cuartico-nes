"""NES-native recreation of the user's tilted Where's Dany title card."""
from PIL import Image, ImageDraw, ImageFilter

PALETTE = bytes([0x10,0x0f,0x00,0x30, 0x10,0x0f,0x21,0x30,
                 0x10,0x0f,0x16,0x30, 0x10,0x08,0x18,0x30])

def build_intro(root, font, pack, first_bank):
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    # Cloudy sky and the recognizable cross above a stone church portico.
    for x,y,w,h in [(4,15,92,34),(126,4,108,34),(162,42,112,40),(-22,65,105,33)]:
        d.ellipse((x,y,x+w,y+h),fill=2)
        d.ellipse((x+6,y+1,x+w-10,y+h-6),fill=0)
    d.line((84,8,84,42),fill=1);d.line((78,19,91,19),fill=1)
    d.polygon([(76,44),(84,31),(94,44)],fill=2,outline=1)
    d.rectangle((75,44,96,61),fill=2,outline=1)
    d.rectangle((80,49,86,61),fill=1)
    d.polygon([(8,138),(235,127),(255,147),(18,162)],fill=1)
    d.polygon([(13,151),(245,139),(255,227),(9,233)],fill=3)
    d.polygon([(47,159),(239,148),(239,177),(46,183)],fill=2)
    for y in (158,166,174):d.line((52,y+9,239,y-4),fill=1)
    for x in range(58,240,15):d.line((x,156,x+6,180),fill=1)
    d.rectangle((111,191,157,225),fill=2)
    d.rectangle((116,195,151,225),fill=1)
    for x in (81,178):
        d.rectangle((x,157,x+14,228),fill=2,outline=1)
        d.rectangle((x+2,158,x+10,227),fill=3)
        for y in range(163,230,12):d.line((x+1,y,x+13,y),fill=1)
    for y in (215,220,225):d.line((9,y,245,y),fill=2)
    for x,y in [(16,207),(29,215),(48,207),(65,217),(101,214),(164,213),(206,207),(222,215),(242,210)]:
        d.ellipse((x,y-6,x+5,y),fill=1)
        d.polygon([(x-1,y+1),(x+6,y+1),(x+8,y+13),(x-2,y+13)],fill=1)
    # Slightly tilted white card, dark edge and cast shadow, matching the reference.
    corners=[(12,64),(237,44),(246,158),(23,182)]
    d.polygon([(x+3,y+4) for x,y in corners],fill=2)
    d.polygon(corners,fill=3,outline=1,width=2)
    blue=Image.new('L',im.size);red=Image.new('L',im.size)
    def letters(mask,string,x,y,scale):
        md=ImageDraw.Draw(mask)
        for ch in string:
            glyph=font.get(ch)
            if ch=='¿':glyph=list(reversed([row[::-1] for row in font['?']]))
            if ch in ('Ó','Á'):glyph=font[{'Ó':'O','Á':'A'}[ch]]
            if glyph:
                for gy,row in enumerate(glyph):
                    for gx,v in enumerate(row):
                        if v=='1':
                            for dx in range(scale):
                                xx=x+gx*scale+dx
                                yy=y+gy*scale-xx//12
                                md.line((xx,yy,xx,yy+scale-1),fill=255)
                if ch in ('Ó','Á'):
                    for step in range(scale*2):
                        xx=x+2*scale+step;yy=y-scale-2-step//2-xx//12
                        md.line((xx,yy,xx,yy+1),fill=255)
            x+=(4 if ch==' ' else 6)*scale
    letters(blue,'¿DÓNDE ESTÁ',30,85,3)
    letters(red,'DANY?',42,119,6)
    for mask in (blue,red):
        shadow=Image.new('L',im.size);shadow.paste(mask,(2,3))
        im.paste(1,(0,0),shadow)
        im.paste(1,(0,0),mask.filter(ImageFilter.MaxFilter(3)))
        im.paste(2,(0,0),mask)
    # One concise prompt, safely inside the visible screen.
    d=ImageDraw.Draw(im);d.rectangle((0,224,255,239),fill=1)
    for pos,ch in enumerate('A / START'):
        for y,row in enumerate(font.get(ch,['00000']*7)):
            for x,v in enumerate(row):
                if v=='1':im.putpixel((92+pos*8+x,225+y),3)
    tiles=[];ids=[];ex=[]
    for y in range(0,240,8):
        for x in range(0,256,8):
            tile=pack(im.crop((x,y,x+8,y+8)))
            if tile not in tiles:tiles.append(tile)
            index=tiles.index(tile);ids.append(index&255)
            pal=1 if blue.crop((x,y,x+8,y+8)).getbbox() else 2 if red.crop((x,y,x+8,y+8)).getbbox() else 0
            if y>=184 and (80<=x<96 or 176<=x<192):pal=3
            ex.append((pal<<6)+first_bank+index//256)
    assert len(tiles)<=512,('intro',len(tiles))
    pages=(len(tiles)+255)//256
    root.joinpath('dany-intro.nam').write_bytes(bytes(ids)+bytes(64))
    root.joinpath('dany-intro.exram').write_bytes(bytes(ex)+bytes(64))
    root.joinpath('dany-intro.pal').write_bytes(PALETTE)
    return b''.join(tiles)+bytes((pages*256-len(tiles))*16),len(tiles)
