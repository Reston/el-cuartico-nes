"""NES-native interpretation of the photographed amber El Cuartico set.

See references/RESEARCH.md for the visual and editorial sources.
Pixels are palette indices, never arbitrary RGB colors.
"""
from PIL import Image, ImageDraw


def portrait(host):
    """32x40 selection busts, each limited to its own 4-entry BG palette."""
    im=Image.new('L',(32,40)); d=ImageDraw.Draw(im)
    # Color cards keep black hair visible against the otherwise black title.
    d.rectangle((0,0,31,30),fill=3)
    if host==0:  # Chucho: short side-part, fine glasses, isolated moustache.
        d.polygon([(2,39),(3,31),(10,27),(21,27),(29,32),(30,39)],fill=3)
        d.rectangle((12,24,19,30),fill=2)
        d.ellipse((7,3,25,27),fill=2)
        d.rectangle((6,14,8,19),fill=2);d.rectangle((24,14,26,19),fill=2)
        d.polygon([(7,13),(6,7),(9,3),(20,1),(25,6),(25,13),(22,10),(21,6),(17,8),(10,9),(9,14)],fill=1)
        d.line((9,13,13,12),fill=1);d.line((19,12,23,13),fill=1)
        d.rectangle((8,14,14,18),outline=3);d.rectangle((18,14,24,18),outline=3)
        d.line((15,15,17,15),fill=1)
        d.point((11,16),fill=1);d.point((21,16),fill=1)
        d.line((16,17,15,20),fill=3)
        d.polygon([(11,21),(14,20),(16,21),(18,20),(22,21),(22,23),(18,22),(15,22),(11,23)],fill=1)
        d.line((14,24,19,24),fill=1)
        d.line((11,29,15,33,20,29),fill=1)
        d.line((16,34,16,39),fill=2)
    elif host==1: # Estefania: long dark waves, pink headband and sleeveless top.
        d.polygon([(3,39),(4,31),(11,27),(20,27),(28,31),(29,39)],fill=3)
        d.ellipse((3,1,29,32),fill=1)
        d.rectangle((12,25,19,31),fill=2)
        d.ellipse((8,6,24,27),fill=2)
        d.polygon([(5,9),(8,3),(20,2),(27,7),(27,10),(21,6),(12,6),(7,11)],fill=3)
        d.polygon([(9,8),(13,6),(10,13),(8,22),(10,28),(7,35),(3,36),(5,27),(3,22),(5,17),(5,11)],fill=1)
        d.polygon([(21,6),(26,9),(27,17),(29,24),(27,29),(29,36),(24,38),(22,33),(24,26),(22,21),(23,15)],fill=1)
        d.line((10,14,14,13),fill=1);d.line((19,13,22,14),fill=1)
        d.line((11,16,13,16),fill=1);d.line((19,16,21,16),fill=1)
        d.point((10,16),fill=1);d.point((22,16),fill=1)
        d.line((16,18,15,20),fill=3)
        d.polygon([(12,22),(20,22),(18,25),(14,25)],fill=3)
        d.line((13,22,19,22),fill=2)
        d.rectangle((6,32,8,39),fill=2);d.rectangle((24,32,26,39),fill=2)
        d.line((11,29,15,33,20,29),fill=2)
    else:  # Daniel: voluminous hair, thick rectangular glasses and full beard.
        d.polygon([(1,39),(2,31),(10,27),(23,27),(30,32),(31,39)],fill=3)
        d.rectangle((12,25,20,31),fill=2)
        d.ellipse((6,3,27,28),fill=2)
        d.polygon([(4,14),(3,7),(7,2),(14,0),(17,2),(23,0),(28,5),(29,12),(25,17),(24,9),(18,6),(11,9),(7,10),(7,17)],fill=1)
        d.rectangle((5,12,14,18),fill=1);d.rectangle((18,12,27,18),fill=1)
        d.rectangle((7,14,12,16),fill=2);d.rectangle((20,14,25,16),fill=2)
        d.line((14,14,18,14),fill=1)
        d.point((10,15),fill=1);d.point((23,15),fill=1)
        d.polygon([(6,19),(10,21),(13,19),(18,19),(23,21),(27,18),(26,25),(21,29),(12,29),(7,25)],fill=1)
        d.line((13,23,20,23),fill=2)
        d.line((10,29,14,32,21,29),fill=1)
    return im


def character(host,frame):
    """16x24 walking silhouettes, 6 hardware sprites and 3 opaque colors."""
    im=Image.new('L',(16,24));d=ImageDraw.Draw(im)
    if host==0:
        d.rectangle((4,1,11,3),fill=1);d.rectangle((3,3,12,5),fill=1)
        d.rectangle((3,5,12,11),fill=2)
        d.line((4,4,8,3,11,4),fill=1)
        d.rectangle((3,6,6,7),outline=3);d.rectangle((9,6,12,7),outline=3)
        d.point((5,6),fill=1);d.point((10,6),fill=1)
        d.rectangle((5,9,10,9),fill=1);d.point((4,10),fill=1);d.point((11,10),fill=1)
        d.line((6,11,9,11),fill=1)
        d.rectangle((3,12,12,18),fill=3);d.line((6,12,7,14,9,12),fill=2)
        d.line((7,15,7,18),fill=2)
    elif host==1:
        d.rectangle((4,1,11,2),fill=1);d.rectangle((2,3,13,16),fill=1)
        d.rectangle((4,4,11,11),fill=2)
        d.line((3,3,5,2,10,2,12,3),fill=3)
        d.rectangle((2,6,3,18),fill=1);d.rectangle((12,5,13,19),fill=1)
        d.point((5,7),fill=1);d.point((10,7),fill=1)
        d.line((6,10,9,10),fill=3)
        d.rectangle((4,12,11,19),fill=3);d.rectangle((6,12,9,13),fill=2)
    else:
        d.rectangle((3,0,12,3),fill=1);d.rectangle((2,2,13,5),fill=1)
        d.rectangle((3,5,12,11),fill=2)
        d.rectangle((2,6,6,8),fill=1);d.rectangle((9,6,13,8),fill=1)
        d.line((6,7,9,7),fill=1);d.point((4,7),fill=2);d.point((11,7),fill=2)
        d.rectangle((3,10,12,12),fill=1);d.rectangle((5,13,10,13),fill=1)
        d.line((6,11,9,11),fill=2)
        d.rectangle((2,14,13,19),fill=3)
    d.rectangle((1,13+frame,2,17+frame),fill=2)
    d.rectangle((13,13-frame,14,17-frame),fill=2)
    d.rectangle((4,19,6,22-frame),fill=1);d.rectangle((9,19,11,21+frame),fill=1)
    d.rectangle((3,22-frame,6,23-frame),fill=3);d.rectangle((9,21+frame,12,22+frame),fill=3)
    return im


def scenes(rect,text):
    studio=Image.new('L',(256,240));d=ImageDraw.Draw(studio)
    # Amber backdrop, dark acoustic panels, cream diagonal stripe and house lamp.
    rect(studio,8,32,240,168,1);rect(studio,16,32,224,32,2)
    for x in (16,48,176,208):
        rect(studio,x,32,24,24,0)
        for dx in range(2,24,4):rect(studio,x+dx,34,1,19,1)
    d.polygon([(64,32),(72,32),(96,56),(88,56)],fill=3)
    rect(studio,96,32,64,24,0)
    text(studio,104,32,'el',3);text(studio,96,40,'cuartico',3)
    # Hanging warm house-shaped practical light, a distinctive set detail.
    rect(studio,163,32,2,5,0)
    d.polygon([(156,43),(164,36),(172,43),(172,55),(156,55)],fill=3)
    rect(studio,16,60,224,4,1)
    # Quiet dark wood floor; no neon wire grid.
    rect(studio,16,64,224,136,1)
    for y in range(80,200,24):
        rect(studio,16,y,224,1,0)
        for x in range(24+(16 if y%48 else 0),236,48):rect(studio,x,y-14,1,14,0)
    for x,y in [(66,76),(168,156),(84,180),(178,84),(62,166)]:rect(studio,x,y,7,1,2)
    # Four grounded pieces of gear, with neutral equipment palettes.
    for x,y in [(24,64),(200,64),(24,136),(200,136)]:
        rect(studio,x,y+3,32,22,0);rect(studio,x+2,y+5,28,17,1)
        rect(studio,x+4,y+7,24,12,0);rect(studio,x+7,y+24,18,2,0)
    # Microphone and mount.
    rect(studio,36,71,8,8,2);rect(studio,38,72,4,6,1)
    d.line((33,76,33,81,40,83,46,80,46,76),fill=2,width=1)
    rect(studio,39,82,2,3,3)
    # Camera body with a lens, two mixers, status lights.
    rect(studio,206,73,13,8,2);d.polygon([(219,75),(225,72),(225,82),(219,79)],fill=1)
    rect(studio,209,70,6,3,1);rect(studio,209,75,3,3,0)
    for x,h in [(30,4),(36,8),(42,3),(48,7)]:
        rect(studio,x,144,1,11,2);rect(studio,x-1,144+h,3,2,3)
    rect(studio,205,149,22,7,2)
    rect(studio,207,139,1,10,3);rect(studio,225,139,1,10,3)
    for x in (209,214,219):rect(studio,x,152,2,1,0)
    # Actual set materials: substantial wooden table, laptop screens, boom mics.
    rect(studio,80,88,96,48,0);rect(studio,82,88,92,38,2)
    rect(studio,84,126,88,7,1);rect(studio,85,133,7,3,0);rect(studio,164,133,7,3,0)
    rect(studio,84,89,88,1,3)
    for x in (88,136):
        rect(studio,x,108,18,10,0);rect(studio,x+2,109,14,7,1)
        rect(studio,x-1,118,20,2,3)
        # Black boom arm and foam microphone.
        d.line((x-5,96,x-2,102,x+2,104),fill=0,width=2)
        rect(studio,x+1,101,5,3,0)
    # Mug with cream rim.
    rect(studio,122,108,6,7,0);rect(studio,122,108,6,1,3)
    d.rectangle((128,109,130,113),outline=0)
    # Chairs outside the existing collision rectangle, a small episode nod.
    for x in (64,179):
        rect(studio,x,111,11,3,0);rect(studio,x+1,114,2,12,0)
        rect(studio,x+8,114,2,12,0);rect(studio,x,125,11,2,0)
    # Wooden kit shelf and clear controls on a charcoal footer.
    rect(studio,104,176,48,24,0);rect(studio,107,180,42,17,2)
    rect(studio,109,182,38,13,1);text(studio,112,184,'REC',3)
    text(studio,24,208,'A: ACCION',3)
    text(studio,24,224,'B: CORRER  START: PAUSA',2)
    def studio_pal(x,y):
        if y<2 or y>=13:return 0
        if y<4:return 1
        if (x in (1,2,3,12,13,14)) and y in (4,5,8,9,10):return 3
        return 2

    title=Image.new('L',(256,240));d=ImageDraw.Draw(title)
    # Small house mark and lower-case wordmark inspired by the show identity.
    rect(title,8,8,240,1,1);rect(title,8,236,240,1,1)
    d.polygon([(112,30),(128,18),(144,30),(144,48),(112,48)],fill=2)
    d.polygon([(128,30),(144,30),(144,48),(128,48)],fill=1)
    text(title,29,56,'el cuartico',3,3)
    text(title,32,88,'NUTRITIVO Y PASTEURIZADO',2)
    text(title,56,112,'!ESTAMOS GRABANDO!',3)
    for host,x in enumerate((48,112,176)):title.paste(portrait(host),(x,144))
    text(title,48,224,'< > ELIGE   START JUEGA',3)
    def title_pal(x,y):
        if 9<=y<=11:
            if 3<=x<=4:return 1
            if 7<=x<=8:return 2
            if 11<=x<=12:return 3
        return 0
    return studio,studio_pal,title,title_pal


def performance_stage(rect,text):
    im=Image.new('L',(256,240));d=ImageDraw.Draw(im)
    rect(im,8,32,240,168,1)
    for x in range(16,240,8):
        rect(im,x,40,4,88,2);rect(im,x+4,40,4,88,1)
    rect(im,64,48,128,88,0)
    d.polygon([(112,56),(144,56),(178,136),(78,136)],fill=1)
    text(im,80,56,'EL SKETCH',3)
    rect(im,16,136,224,16,2);rect(im,16,136,224,2,3)
    for x in range(24,240,16):rect(im,x,150,4,2,3)
    rect(im,16,160,224,40,0);rect(im,24,181,208,1,1)
    d.rectangle((48,166,80,194),outline=3)
    rect(im,47,165,34,1,2);rect(im,47,195,34,1,2)
    text(im,120,208,'<',2);text(im,64,224,'A B < >   START',3)
    def pal(x,y):
        if y<2 or y>=10:return 0
        if y>=8:return 2
        return 1 if x<4 or x>=12 else 3
    return im,pal
