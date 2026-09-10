"""Original MMC5 art: joint four-frame tile encoding and scene-specific palettes."""
from ui_font import draw_ui_glyph
from PIL import Image, ImageDraw
from art import scenes
from likeness import bust, character, performer, repairer, plaza_person, menu_portrait


def studio_frames(rect,text):
    base,pal,_,_=scenes(rect,text)
    # Fine wood grain, soft carpet, bevelled furniture and a framed studio wall.
    for y in range(68,200,16):
        for x in range(16,240,32):
            if (80<=x<176 and 88<=y<136) or (16<=x<64 or 192<=x<240) and (64<=y<96 or 136<=y<168) or 104<=x<152 and y>=176:continue
            for dx in (2,3,4,10):
                if base.getpixel((x+dx,y))==1:base.putpixel((x+dx,y),0)
    d=ImageDraw.Draw(base)
    for x in (8,240):
        rect(base,x,32,8,168,0);rect(base,x+1,32,2,168,2);rect(base,x+4,32,1,168,1)
    for y in (58,61):rect(base,16,y,224,1,3 if y==58 else 0)
    for x in (88,136):
        rect(base,x+2,110,14,5,0);rect(base,x+3,113,2,1,3)
    # Dense acoustic foam texture retains the warm set, avoiding a neon restyle.
    for x in (16,48,176,208):
        for yy in (36,44,52):
            for xx in range(x+2,x+22,4):rect(base,xx,yy,2,1,2)
    out=[]
    for f in range(4):
        im=base.copy()
        for x in (92,140):
            for i in range(4):
                h=1+(f+i*2)%4;rect(im,x+i*3,115-h,2,h,2+(i==3))
        rect(im,160,43,8,9,3 if f<2 else 2)
        rect(im,126,105-f%2,1,2,3) # rising steam from the mug
        out.append(im)
    return out,pal


def title_frames(rect,text):
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    # A warm marquee framed by the studio's acoustic texture.
    for x in (8,240):
        rect(im,x,8,8,224,1)
        for y in range(12,232,8):rect(im,x+2,y,3,1,2)
    rect(im,16,8,224,2,2);rect(im,16,232,224,2,2)
    for x in range(24,240,16):rect(im,x,16,8,1,1)
    d.polygon([(112,40),(112,28),(128,16),(144,28),(144,40)],fill=2)
    d.polygon([(128,28),(144,28),(144,40),(128,40)],fill=1)
    rect(im,124,30,7,10,3)
    text(im,29,48,'el cuartico',3,3)
    text(im,40,80,'ESTAMOS GRABANDO!',2)
    rect(im,40,104,176,1,1)
    for h,x in enumerate((32,96,160)):
        im.paste(menu_portrait(h,gear=True),(x,120))
    text(im,40,224,'< > ELIGE  A: JUEGA',3)
    # MMC5 assigns the skin palette per 8x8 tile; clothes have host colors.
    def pal8(x,y):
        if 15<=y<21 and 4<=x<28:return 1
        if 21<=y<23 and 4<=x<28:return (3,2,0)[(x-4)//8]
        return 0
    def pal(x,y):return pal8(x*2,y*2)
    frames=[]
    for f in range(4):
        q=im.copy()
        for h,x in enumerate((32,96,160)):
            q.paste(menu_portrait(h,blink=f==h+1,gear=True),(x,120))
        for x in (24,224):
            rect(q,x,48,4,4,3 if f%2 else 2)
            rect(q,x,88,4,4,2 if f%2 else 3)
        frames.append(q)
    return frames,pal8


def stage_frames(rect,text):
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    # Layered theatre proscenium, gold piping and a starry violet backdrop.
    rect(im,8,32,240,128,1)
    for x in range(16,240,8):
        rect(im,x,40,3,104,2);rect(im,x+3,40,1,104,3);rect(im,x+5,40,3,104,1)
    rect(im,56,56,144,80,0)
    d.polygon([(88,56),(100,56),(138,136),(62,136)],fill=1)
    d.polygon([(164,56),(176,56),(198,136),(116,136)],fill=1)
    for x in range(24,240,32):
        d.polygon([(x,32),(x+31,32),(x+27,50),(x+16,56),(x+4,50)],fill=2)
        d.line((x+4,49,x+16,54,x+27,49),fill=3)
    text(im,80,64,'EL SKETCH',3)
    for x in (16,232):
        rect(im,x,56,6,80,1);rect(im,x,56,2,80,3)
    for y,c in [(136,3),(138,2),(146,1),(149,3),(152,2)]:rect(im,16,y,224,2,c)
    for x in range(24,240,16):rect(im,x,140,8,1,1)
    d.ellipse((88,130,167,145),fill=2)
    d.arc((91,130,164,143),0,180,fill=3)
    # Music lane remains uncluttered and preserves the tested timing coordinates.
    rect(im,16,164,224,34,1);rect(im,20,166,216,30,0)
    rect(im,24,181,208,1,1)
    d.rectangle((48,166,80,194),outline=3)
    rect(im,47,165,34,1,2);rect(im,47,195,34,1,2)
    # Audience silhouettes and balcony lights give a sense of a live performance.
    for x in range(16,240,16):
        d.ellipse((x,207,x+9,216),fill=1);rect(im,x-2,215,14,5,1)
    text(im,56,224,'A B < >  START',3)
    def pal(x,y):
        if y<2 or y>=10:return 0
        if y>=8:return 2
        return 1 if x<4 or x>=12 else 3
    frames=[]
    for f in range(4):
        q=im.copy()
        for i,(x,y) in enumerate([(72,88),(176,80),(88,112),(168,120)]):
            c=3 if i==f else 1
            rect(q,x,y,5,1,c);rect(q,x+2,y-2,1,5,c)
        for i,x in enumerate(range(24,240,16)):rect(q,x,150,4,2,3 if i%4==f else 1)
        audience=ImageDraw.Draw(q)
        for i,x in enumerate(range(16,240,16)):
            if i%4==f:
                audience.line((x-2,216,x-5,207,x-7,205),fill=1,width=2)
                audience.line((x+10,216,x+12,208,x+14,206),fill=1,width=2)
        frames.append(q)
    return frames,pal


def plaza_frames(rect,text,scene,district=0):
    # Same walkable square, three distinct storefront/landscape compositions.
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    pals=[[0]*16 for _ in range(15)]
    def region(x,y,w,h,p):
        for yy in range(y//16,(y+h+15)//16):
            for xx in range(x//16,(x+w+15)//16):
                if yy<15 and xx<16:pals[yy][xx]=p
    text(im,8,8,('PLAZA CUARTICO','PLAZA DEL MERCADO','PLAZA DE LAS FLORES')[scene],1)
    rect(im,0,24,256,1,2)
    rect(im,0,224,256,1,2);text(im,16,224,'+ MUEVE A BUSCA B LUPA',1)
    # Two substantial storefronts: tiled roofs, fascia, shuttered windows and doors.
    labels=[('CAFE','LIBROS'),('FRUTAS','PAN'),('FLORES','CAFE')][scene]
    if district:labels=[('MUSICA','HELADOS'),('TEATRO','ARTE'),('CINE','DISCOS')][district-1]
    for x,label in [(0,labels[0]),(176,labels[1])]:
        rect(im,x,48,80,48,3)
        for yy in (48,52,56):
            rect(im,x,yy,80,1,1)
            for xx in range(x+(4 if yy==52 else 0),x+80,8):rect(im,xx,yy+1,1,3,1)
        rect(im,x,60,80,12,2);text(im,x+8,64,label,1)
        for xx in (x+8,x+56):
            rect(im,xx,76,16,14,1);rect(im,xx+2,78,12,8,2)
            rect(im,xx+7,78,1,8,3);rect(im,xx+2,81,12,1,3)
            rect(im,xx-2,90,20,2,1)
        rect(im,x+32,76,16,20,1);rect(im,x+34,78,12,16,2)
        rect(im,x+43,84,1,2,3);rect(im,x+30,94,20,2,1)
    # Recessed windows, projecting sills and striped canvas awnings.
    for x in (0,176):
        for xx in (x+8,x+56):
            rect(im,xx+2,78,3,8,1)
            rect(im,xx+3,79,3,2,3)
            rect(im,xx-2,89,20,1,2);rect(im,xx-1,91,18,2,1)
        for xx in range(x,x+80,8):
            rect(im,xx,71,4,4,1);rect(im,xx+4,71,4,3,3)
        rect(im,x+34,78,2,15,3);rect(im,x+30,95,24,1,1)
    # Central arch frames the fountain while leaving the reference portrait clear.
    d.arc((96,48,159,111),180,360,fill=1,width=5)
    d.arc((99,51,156,108),180,360,fill=3,width=2)
    for x in (96,152):
        rect(im,x,78,8,18,1);rect(im,x+1,78,5,16,3)
        for y in (81,88,94):rect(im,x+1,y,5,1,2)
    d.ellipse((120,56,135,71),fill=2,outline=1)
    text(im,124,60,'C',1)
    rect(im,96,80,64,9,3);text(im,96,80,'CUARTICO',1)
    # Repeated paving stones: small highlights rather than a bright blank field.
    for y in range(100,224,16):
        for x in range(0,256,32):
            rect(im,x+(8 if y%32 else 0),y,7,1,2)
            rect(im,x+(8 if y%32 else 0)+8,y+1,1,2,3)
    # Low shaded planters with clustered leaves, trunks and edge highlights.
    for x in (0,224):
        region(x,128,32,32,2)
        d.rectangle((x,152,x+31,159),fill=1);rect(im,x+2,152,28,2,3)
        d.rectangle((x+14,143,x+17,153),fill=1)
        for dx,dy in [(2,134),(8,128),(17,130),(20,138),(7,140)]:
            d.ellipse((x+dx,dy,x+dx+11,dy+11),fill=2)
            rect(im,x+dx+3,dy+2,5,2,3)
        rect(im,x+23,142,5,4,1)
        d.line((x+7,145,x+12,140,x+19,139),fill=1)
        rect(im,x+3,156,25,1,2)
    # Fountain basin and jets use their own blue subpalette.
    region(96,128,48,48,3)
    d.ellipse((96,144,143,171),fill=1);d.ellipse((98,142,141,165),fill=3)
    d.ellipse((102,145,137,161),fill=2)
    rect(im,118,128,4,27,3);rect(im,110,133,20,4,1);rect(im,112,132,16,2,3)
    for xx in (106,132):rect(im,xx,138,2,15,3)
    d.arc((96,144,143,171),0,180,fill=2,width=2)
    d.arc((103,144,136,159),10,170,fill=3)
    rect(im,113,130,14,2,2)
    for x,y in [(48,144),(176,160)]:
        for dy in (0,3,8):rect(im,x,y+dy,32,2,1)
        rect(im,x+3,y+10,2,5,1);rect(im,x+27,y+10,2,5,1)
        rect(im,x+1,y+1,30,1,3)
        rect(im,x+1,y+9,30,1,2)
        rect(im,x+4,y+2,1,7,2);rect(im,x+26,y+2,1,7,2)
    for x,y in [(32,112),(192,128)]:
        d.ellipse((x,y,x+15,y+7),fill=3);d.line((x,y+4,x+15,y+4),fill=2)
        rect(im,x+6,y+8,3,13,1);rect(im,x+2,y+19,11,2,1)
    for x in (0,224):
        region(x,208,32,16,2);rect(im,x,208,32,16,1)
        for dx in (4,12,20,28):
            rect(im,x+dx,212,2,8,2);rect(im,x+dx-1,211,4,3,3)
    # Scene-specific detail changes are readable even with the same search rules.
    if scene==1:
        for x in (0,176):
            for dx in range(0,80,8):rect(im,x+dx,72,4,3,2)
    if scene==2:
        for x in (8,184):
            for dx in (0,56):
                rect(im,x+dx,90,16,5,2)
                for fx in range(2,16,4):rect(im,x+dx+fx,88,2,3,1)
    # Clear character slots: each 16x32 patch must keep the same ground color
    # as the character's transparent pixels and obey 16x16 NES attributes.
    xs=[16,48,80,112,160,192,224,64,176,32,96,128,208,16,64,160,208,112,144,80,160,48,224,192]
    ys=[96,96,96,96,96,96,96,112,112,144,176,176,144,160,176,176,176,192,112,128,144,160,176,192]
    # Each district has a different landmark, retaining the clear hiding paths.
    if district:
        region(96,128,48,48,0)
        rect(im,96,128,48,48,0)
        if district==1:
            # Bandstand, speakers and a striped canopy.
            d.polygon([(98,145),(120,126),(142,145)],fill=2)
            rect(im,100,145,40,3,3)
            for xx in (102,136):rect(im,xx,148,3,19,1)
            rect(im,100,167,40,6,1);rect(im,108,153,8,12,2);rect(im,127,153,8,12,2)
        elif district==2:
            # Statue and stepped stone pedestal.
            d.ellipse((114,128,125,138),fill=3)
            d.polygon([(113,139),(126,139),(131,158),(108,158)],fill=2)
            rect(im,105,159,31,6,1);rect(im,100,166,41,7,2)
        else:
            # Flower stall with colorful potted plants.
            rect(im,99,136,42,6,2);rect(im,102,142,3,26,1);rect(im,135,142,3,26,1)
            for xx in (109,119,129):
                rect(im,xx,156,7,10,1);d.ellipse((xx-2,147,xx+8,157),fill=3)
            rect(im,99,168,42,5,2)
    # Each neighborhood has a recognizable silhouette and its own street surface.
    if scene==1:
        for x in (8,184):
            d.polygon([(x,47),(x+32,35),(x+64,47)],fill=2)
            rect(im,x+4,45,56,2,1)
        for x in (88,160):
            rect(im,x,128,4,28,1);rect(im,x-2,125,8,5,2)
    if scene==2:
        # Hanging festival bunting above the lanes and a tiled garden promenade.
        d.line((0,40,80,43,176,40,255,43),fill=1)
        for x in range(8,256,24):
            d.polygon([(x,41),(x+7,41),(x+3,46)],fill=2)
        for x in range(40,216,16):
            rect(im,x,218,8,2,1)
    if district==2:
        # Sculpture court: long stone plinth instead of a round fountain.
        rect(im,96,166,48,8,1);rect(im,100,167,40,2,3)
        for x in (104,128):rect(im,x,172,8,2,2)
    if district==3:
        # Flower arcade, with trellis work along the outside walls.
        for x in (0,240):
            for y in range(98,126,8):
                d.line((x,y,x+15,y+7),fill=2)
                d.line((x+15,y,x,y+7),fill=2)
    # Foreground flower beds frame the square, without filling the search lanes.
    for x,w in [(0,80),(208,48)]:
        region(x,208,w,16,2)
        rect(im,x,214,w,10,1);rect(im,x,213,w,2,3)
        for xx in range(x+4,x+w,8):
            rect(im,xx,217,2,5,2)
            d.ellipse((xx-2,210,xx+3,214),fill=2)
            rect(im,xx,210,1,2,3)
    # Two compact streetside planters occupy gaps between the hiding slots.
    for x,y in [(80,176),(144,176)]:
        region(x,y,16,32,2)
        d.ellipse((x+2,y+13,x+13,y+25),fill=1)
        rect(im,x+2,y+14,12,2,3)
        d.ellipse((x,y+3,x+15,y+14),fill=2)
        d.line((x+4,y+6,x+10,y+5),fill=3)
    # Keep every possible face unobstructed, including the denser remix crowd.
    for x,y in zip(xs,ys):rect(im,x,y,16,24,0)
    frames=[]
    for f in range(4):
        q=im.copy()
        # Travelling water glints and leaf highlights are animated by CHR banks.
        for x,y in ([] if district else [(108,150),(120,156),(130,149)]):rect(q,x+f%2,y+(f//2),5,1,3)
        for x in (0,224):rect(q,x+12+f%2,137,3,1,3)
        for i,(x,y) in enumerate([(88,208),(168,208)]):
            rect(q,x,y+2,5,3,1);rect(q,x+4,y,3,3,1)
            if f%2:rect(q,x-1,y+1,3,1,1)
        if district&1:
            # Mirror the street and its hiding paths together, keeping all signs readable.
            q.paste(q.crop((0,96,256,224)).transpose(Image.Transpose.FLIP_LEFT_RIGHT),(0,96))
        if scene:
            # Empty, high-contrast strips reserve real space for exit arrows.
            border=ImageDraw.Draw(q)
            for x,label in ((0,labels[0]),(176,labels[1])):
                border.rectangle((x,56,x+79,63),fill=2)
                text(q,x+8,56,label,1)
            border.rectangle((0,64,15,223),fill=0)
            border.rectangle((240,64,255,223),fill=0)
            border.rectangle((0,64,255,71),fill=0)
            border.rectangle((0,216,255,223),fill=0)
            border.line((15,72,15,215),fill=1)
            border.line((240,72,240,215),fill=1)
            border.line((16,71,239,71),fill=1)
            border.line((16,216,239,216),fill=1)
            if district&1:
                border.polygon([(2,143),(9,136),(9,140),(13,140),(13,146),(9,146),(9,150)],fill=1)
            else:
                border.polygon([(253,143),(246,136),(246,140),(242,140),(242,146),(246,146),(246,150)],fill=1)
            if scene==2:
                if district>=2:
                    border.polygon([(127,64),(120,69),(124,69),(124,75),(130,75),(130,69),(134,69)],fill=1)
                else:
                    border.polygon([(127,223),(120,218),(124,218),(124,214),(130,214),(130,218),(134,218)],fill=1)
        frames.append(q)
    if district&1:
        xs=[240-x for x in xs]
        for y in range(6,14):pals[y].reverse()
    if scene:
        for y in range(4,14):pals[y][0]=pals[y][15]=0
    return frames,lambda x,y:pals[y][x] if y<15 else 0,xs,ys


def build(root,FONT,rect,text,pack,sprites):
    import json
    banks=[];budgets={};portrait_banks=[]
    search_tiles=[]
    for kind in range(6):
        person=plaza_person(kind)
        for y in range(0,24,8):
            for x in range(0,16,8):search_tiles.append(pack(person.crop((x,y,x+8,y+8))))
    def encode(name,frames,pal,people=False):
        # The key includes every animation frame so shared tiles never diverge.
        font_ink=1 if people else 3
        tilekeys=[(bytes(16),)*4 for _ in range(128)]
        for ch in FONT:
            q=Image.new('L',(8,8))
            if name=='title':draw_ui_glyph(q,ch,font_ink,text)
            else:text(q,0,0,ch,font_ink)
            tilekeys[ord(ch)]=(pack(q),)*4
        free=[i for i in range(1,128) if chr(i) not in FONT and i!=32]
        ids=[]
        for y in range(0,240,8):
            for x in range(0,256,8):
                k=tuple(pack(im.crop((x,y,x+8,y+8))) for im in frames)
                if k not in tilekeys:
                    if free:tilekeys[free.pop(0)]=k
                    else:tilekeys.append(k)
                ids.append(tilekeys.index(k))
        extended=name=="title"
        limit=512 if extended else 220 if people else 256
        assert len(tilekeys)<=limit,(name,len(tilekeys),limit)
        attrs=[]
        for ay in range(8):
            for ax in range(8):
                attrs.append(sum((pal(ax*4+dx*2,ay*4+dy*2) if extended else pal(ax*2+dx,ay*2+dy))<<((dy*2+dx)*2) for dy in range(2) for dx in range(2)))
        root.joinpath(name+'.nam').write_bytes(bytes([i&255 for i in ids]+attrs))
        if extended:
            # Two tile pages on one screen. ExRAM selects a bank AND a palette
            # independently for every 8x8 cell. Dynamic text rows use font page 0.
            # These rows are replaced with ASCII text by hub()/ending(). Their
            # bank must follow the runtime text, not the baked placeholder art.
            text_rows={10,12,14,24,26,28}
            ex=[0 if i//32 in text_rows else (pal(i%32,i//32)<<6)+(26 if t>=256 else 0) for i,t in enumerate(ids)]
            root.joinpath('title.exram').write_bytes(bytes(ex+[0]*64))
            asm=['; Generated: only animated title cells change during vblank.']
            for i,t in enumerate(ids):
                if len(set(tilekeys[t]))>1:
                    asm+=[' lda _art_bank',' clc',' adc #'+str(ex[i]),' sta $'+format(0x5c00+i,'04x')]
            root.joinpath('title-anim.inc').write_text('\n'.join(asm)+'\n')
        for f in range(4):
            b=b''.join(k[f] for k in tilekeys)+bytes((limit-len(tilekeys))*16)
            if people:b+=b''.join(search_tiles)
            if extended:
                banks.append(b[:4096]);portrait_banks.append(b[4096:8192])
            else:banks.append(b)
        budgets[name]=len(tilekeys);print(name,len(tilekeys),'/',limit)
    encode('title',*title_frames(rect,text))
    encode('studio',*studio_frames(rect,text))
    encode('stage',*stage_frames(rect,text))
    for scene in range(3):
        frames,pal,xs,ys=plaza_frames(rect,text,scene)
        encode('plaza'+str(scene),frames,pal,True)
    root.joinpath('plaza.nam').write_bytes(root.joinpath('plaza0.nam').read_bytes())
    # Sprite bank: preserve control icons, add smoother walks and a 24x40 performer.
    while len(sprites)<56:sprites.append(bytes(16))
    for h in range(3):
        for f in (0,1):
            q=character(h,f).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            for y in range(0,24,8):
                for x in range(0,16,8):sprites.append(pack(q.crop((x,y,x+8,y+8))))
    while len(sprites)<96:sprites.append(bytes(16))
    for pose in range(4):
        q=performer(pose)
        for y in range(0,40,8):
            for x in range(0,24,8):sprites.append(pack(q.crop((x,y,x+8,y+8))))
    # Larger note badges remain centered on the exact original hit coordinates.
    for symbol in range(6):
        q=Image.new('L',(16,16));d=ImageDraw.Draw(q)
        d.rounded_rectangle((0,0,15,15),radius=3,fill=1,outline=2)
        glyph=Image.new('L',(8,8));data=sprites[42+symbol]
        for yy in range(8):
            for xx in range(8):
                v=((data[yy]>>(7-xx))&1)|(((data[yy+8]>>(7-xx))&1)<<1)
                if v:q.putpixel((xx+4,yy+4),3)
        for yy in (0,8):
            for xx in (0,8):sprites.append(pack(q.crop((xx,yy,xx+8,yy+8))))
    for ch in 'BRAVOIEN':
        q=Image.new('L',(8,8));text(q,0,0,ch);sprites.append(pack(q))
    for f in range(4):
        q=repairer(f)
        for yy in range(0,32,8):
            for xx in range(0,24,8):sprites.append(pack(q.crop((xx,yy,xx+8,yy+8))))
    extra=[
        ['00020000','00030000','00232000','23333320','00232000','00030000','00020000','00000000'],
        ['11000110','11101110','01111100','00111000','01111100','11101110','11000110','00000000'],
        ['01101100','13313310','13333310','01333100','00131000','00010000','00000000','00000000'],
        ['01101100','10010010','10000010','01000100','00101000','00010000','00000000','00000000'],
        ['00000000','00000000','03333330','03332230','03333330','00000000','00000000','00000000'],
        ['00000000','00000000','03333330','03112230','03333330','00000000','00000000','00000000'],
    ]
    for rows in extra:
        q=Image.new('L',(8,8))
        for yy,row in enumerate(rows):
            for xx,v in enumerate(row):q.putpixel((xx,yy),int(v))
        sprites.append(pack(q))
    for ch in '0123456789X-!':
        q=Image.new('L',(8,8));text(q,0,0,ch);sprites.append(pack(q))
    q=Image.new('L',(8,8));d=ImageDraw.Draw(q)
    d.polygon([(3,0),(4,2),(7,2),(5,4),(6,7),(3,5),(0,7),(1,4),(0,2),(2,2)],fill=2)
    d.point((3,3),fill=3);sprites.append(pack(q))
    # Four shared tiles for a flapping bird and a rolling market cart. They
    # occupy unused reverse-walk tiles and are copied into the lens bank too.
    for f in range(2):
        q=Image.new('L',(8,8));d=ImageDraw.Draw(q)
        d.line((0,2 if f else 5,3,4,4,4,7,2 if f else 5),fill=1)
        d.line((3,4,4,5),fill=3)
        sprites[60+f]=pack(q)
    q=Image.new('L',(16,8));d=ImageDraw.Draw(q)
    d.rectangle((2,0,13,4),fill=3);d.line((0,0,1,5,14,5),fill=1)
    for x in (3,11):d.rectangle((x,6,x+2,7),fill=1)
    d.line((6,1,6,3),fill=2);d.line((10,1,10,3),fill=2)
    sprites[62]=pack(q.crop((0,0,8,8)));sprites[63]=pack(q.crop((8,0,16,8)))
    assert len(sprites)==256
    banks.append(b''.join(sprites)+bytes((256-len(sprites))*16))
    # Magnifier bank keeps shared icons but replaces the performer with enlarged
    # face combinations. It is used only while B is held in Daniel's search.
    lens=sprites[:64]
    lens[24:28]=search_tiles[:4]
    for i,ch in enumerate('LUPA'):
        q=Image.new('L',(8,8));text(q,0,0,ch);lens[56+i]=pack(q)
    combos=[(2,2),(0,0),(1,1),(2,0),(0,2),(1,0)]
    for top,bottom in combos:
        # The lens gets its own detailed face drawing, retaining each decoy's
        # hair/glasses and facial-hair combination from the small plaza sprite.
        q=bust(top).crop((12,0,52,48))
        q.paste(bust(bottom).crop((12,32,52,48)),(0,32))
        q=q.resize((32,32),Image.Resampling.NEAREST).point(lambda v:(0,1,3,2)[v%4])
        # Open corners keep the silhouette round rather than a solid box.
        mask=Image.new('1',(32,32));ImageDraw.Draw(mask).ellipse((0,0,31,31),fill=1)
        canvas=Image.new('L',(32,32));canvas.paste(q,(0,0),mask);q=canvas
        for yy in range(0,32,8):
            for xx in range(0,32,8):lens.append(pack(q.crop((xx,yy,xx+8,yy+8))))
    while len(lens)<236:lens.append(bytes(16))
    lens.extend(sprites[236:256])
    banks.append(b''.join(lens))
    banks.extend(portrait_banks)
    for scene,district in [(1,1),(2,1),(2,2),(2,3)]:
        frames,pal,xs,ys=plaza_frames(rect,text,scene,district)
        encode('district'+str(scene)+str(district),frames,pal,True)
    # Search-only sprite bank keeps the reference face consistent with the crowd.
    search_sprites=sprites[:];search_sprites[24:28]=search_tiles[:4]
    # Optional episode-two props occupy otherwise unused search-only sprite tiles.
    for item in range(2):
        q=Image.new('L',(16,16));d=ImageDraw.Draw(q)
        if item==0:
            d.ellipse((4,0,11,8),fill=2,outline=1)
            d.line((5,3,10,3),fill=1);d.line((5,5,10,5),fill=1)
            d.rectangle((7,8,8,14),fill=1);d.line((4,15,11,15),fill=1)
        else:
            d.rectangle((2,0,13,15),fill=2,outline=1)
            for y in (4,7,10):d.line((5,y,10,y),fill=1)
            d.point((11,13),fill=2)
        for j in range(4):
            xx,yy=(j&1)*8,(j>>1)*8
            search_sprites[72+item*4+j]=pack(q.crop((xx,yy,xx+8,yy+8)))
    # The live routine shares this variant sprite page; these slots are not used
    # by search cursors, the lens, or Estefania's full-size performer.
    for tile in (80,81):
        q=Image.new('L',(8,8));d=ImageDraw.Draw(q)
        d.rectangle((0,3,7 if tile==80 else 5,4),fill=3)
        if tile==81:d.rectangle((5,1,6,6),fill=2)
        search_sprites[tile]=pack(q)
    assert len(banks)==46
    banks.append(b''.join(search_sprites))
    from dany_intro import build_intro
    intro,used=build_intro(root,FONT,pack,len(banks))
    for offset in range(0,len(intro),4096):banks.append(intro[offset:offset+4096])
    budgets['dany_intro']=used;print('dany_intro',used,'/ 512')
    from presentation import build_presentation
    slate,used=build_presentation(root,FONT,text,pack)
    banks.append(slate);budgets['presentation']=used
    print('presentation',used,'/ 256')
    from character_intros import build_card
    for host,name in enumerate(('chucho_intro','estefania_intro')):
        card,used=build_card(root,FONT,pack,host,len(banks))
        banks.extend(card[offset:offset+4096] for offset in range(0,len(card),4096))
        budgets[name]=used;print(name,used,'/ 512')
    root.joinpath('mmc5.chr').write_bytes(b''.join(banks)+bytes(262144-len(banks)*4096))
    root.joinpath('art-budget.json').write_text(json.dumps({'banks_used':len(banks),'backgrounds':budgets,'sprite_tiles':len(sprites),'chr_bytes':262144,'extended_attributes':'title/ending/character intros, 8x8 palettes and two simultaneous tile pages'},indent=2))
