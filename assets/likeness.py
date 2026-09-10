"""Hand-pixelled host art, referenced to the photographs supplied during development.
Native palette indices: these assets are encoded directly for the NES PPU.
"""
from PIL import Image, ImageDraw


def bust(host,blink=False,gear=False):
    im=Image.new('L',(64,64));d=ImageDraw.Draw(im)
    # An open oval of studio light replaces the old rectangular color cards.
    d.ellipse((5,2,58,61),fill=2)
    if host==0:
        d.polygon([(5,63),(8,54),(20,47),(27,44),(41,44),(53,52),(58,63)],fill=2)
        d.polygon([(26,42),(26,49),(33,54),(40,48),(39,40)],fill=2)
        d.polygon([(20,49),(26,47),(32,55),(27,61)],fill=1)
        d.polygon([(40,47),(47,50),(38,61),(34,55)],fill=1)
        d.polygon([(31,54),(35,54),(38,63),(29,63)],fill=3)
        d.ellipse((17,6,47,44),fill=3)
        d.ellipse((14,22,21,31),fill=3);d.ellipse((43,22,49,31),fill=2)
        d.polygon([(42,13),(47,21),(46,34),(41,41),(34,44),(28,42),(40,39),(43,31)],fill=2)
        d.polygon([(16,22),(15,14),(17,8),(23,4),(37,2),(45,7),(48,14),(46,22),(43,20),(42,11),(36,10),(29,13),(21,13),(20,22)],fill=1)
        d.line((20,9,28,6,37,6),fill=2)
        d.line((20,19,26,18),fill=1);d.line((35,18,41,19),fill=1)
        # Thin ROUND wire frames, with skin still visible through the lenses.
        d.ellipse((18,20,29,28),outline=2);d.ellipse((33,20,44,28),outline=2)
        d.line((29,23,33,23),fill=1);d.point((23,24),fill=1);d.point((38,24),fill=1)
        d.line((31,24,30,29,33,30),fill=2)
        d.polygon([(23,33),(25,31),(30,31),(32,32),(35,31),(40,33),(40,35),(35,34),(31,34),(26,34),(22,35)],fill=1)
        d.arc((25,32,39,40),0,180,fill=1)
        d.line((28,37,36,37),fill=3)
        d.line((16,53,12,62),fill=2);d.line((48,53,52,62),fill=2)
    elif host==1:
        # Photo reference: off-center part, long dark hair, almond eyes and
        # a tapered chin. Keep neck skin above the jacket palette boundary.
        d.polygon([(13,18),(15,10),(21,5),(29,2),(38,3),(47,8),(51,18),(49,31),(53,43),(51,53),(55,63),(10,63),(13,53),(10,43),(13,31)],fill=1)
        d.polygon([(9,63),(13,54),(24,48),(40,48),(50,54),(55,63)],fill=3)
        d.polygon([(25,48),(39,48),(43,63),(22,63)],fill=1)
        d.polygon([(25,42),(38,41),(38,47),(33,50),(27,47)],fill=2)
        d.polygon([(22,12),(29,8),(37,9),(43,15),(45,25),(43,34),(39,40),(33,44),(28,43),(23,39),(20,33),(19,23)],fill=3)
        d.polygon([(41,18),(44,23),(43,33),(39,39),(33,43),(28,42),(34,40),(39,34)],fill=2)
        d.polygon([(18,28),(16,21),(18,13),(23,7),(31,4),(29,9),(25,13),(22,18),(21,28)],fill=1)
        d.polygon([(31,4),(41,6),(48,13),(49,23),(45,34),(43,28),(43,19),(39,13),(34,10)],fill=1)
        d.line((20,14,23,10,28,7),fill=2)
        d.line((33,6,39,8,43,12),fill=2)
        d.line((23,21,26,20,29,21),fill=1)
        d.line((35,21,38,20,41,21),fill=1)
        d.line((23,25,25,24,28,24,29,25),fill=1)
        d.line((35,25,37,24,40,24,41,25),fill=1)
        d.point((26,25),fill=1);d.point((38,25),fill=1)
        d.line((32,25,31,29,33,30),fill=2)
        d.line((25,31,27,32),fill=2)
        d.polygon([(26,33),(30,34),(34,33),(39,32),(37,37),(33,39),(29,38)],fill=1)
        d.line((28,34,36,34),fill=3);d.line((29,35,35,35),fill=3)
        d.line((30,38,34,38),fill=2)
        # Denim lapels and seams; hair falls over the jacket, not a dress.
        d.polygon([(23,48),(28,52),(25,57),(21,53),(22,63),(16,63),(17,54)],fill=2)
        d.polygon([(40,48),(36,53),(40,57),(43,53),(45,63),(49,63),(47,54)],fill=2)
        d.line((21,54,24,57,23,62),fill=3)
        d.line((43,54,40,58,42,63),fill=3)
        d.polygon([(14,30),(20,30),(19,39),(22,47),(20,55),(18,63),(13,63),(15,53),(13,44)],fill=1)
        d.polygon([(44,30),(49,29),(48,39),(51,47),(48,56),(50,63),(43,63),(44,54),(42,45)],fill=1)
    else:
        d.polygon([(4,63),(7,54),(21,47),(40,45),(54,53),(61,63)],fill=3)
        d.polygon([(25,43),(25,48),(33,54),(41,47),(39,40)],fill=2)
        d.arc((22,43,44,57),5,170,fill=1,width=2)
        d.ellipse((17,8,48,43),fill=3)
        d.ellipse((14,22,20,31),fill=2);d.ellipse((45,22,50,31),fill=2)
        d.polygon([(16,25),(12,18),(13,11),(17,6),(25,3),(36,2),(44,5),(49,10),(51,16),(48,25),(44,23),(43,14),(37,11),(32,14),(25,16),(20,15),(20,24)],fill=1)
        d.line((18,12,25,8,33,7,41,8),fill=2)
        d.line((19,19,27,18),fill=1);d.line((36,18,44,19),fill=1)
        d.rounded_rectangle((16,20,29,29),radius=2,outline=1,width=2)
        d.rounded_rectangle((33,20,47,29),radius=2,outline=1,width=2)
        d.line((29,23,33,23),fill=1,width=2)
        d.point((23,25),fill=1);d.point((39,25),fill=1)
        d.line((31,26,30,31,34,31),fill=2)
        d.polygon([(17,29),(22,32),(26,31),(31,32),(36,31),(42,32),(48,27),(47,36),(43,43),(36,48),(28,48),(22,43),(18,37)],fill=1)
        d.line((26,36,38,36),fill=3);d.line((29,38,35,38),fill=2)
        d.line((23,40,27,43),fill=2);d.line((40,40,37,44),fill=2)
        d.line((14,54,11,62),fill=1);d.line((51,55,55,62),fill=1)
    if blink:
        if host==0:
            for x in (23,38):
                d.point((x,24),fill=3);d.line((x-2,25,x+1,25),fill=1)
        elif host==1:
            for x in (26,38):
                d.rectangle((x-2,24,x+2,26),fill=3)
                d.arc((x-3,22,x+3,26),0,180,fill=1)
        else:
            for x in (23,39):
                d.point((x,25),fill=3);d.line((x-2,26,x+1,26),fill=1)
    if gear:
        # The accepted cartoon cover's headphones and microphone, at native size.
        d.arc((11,0,53,39),183,354,fill=1,width=3)
        d.arc((12,1,52,38),194,340,fill=2)
        for x in (10,49):
            d.rounded_rectangle((x,20,x+5,34),radius=2,fill=1)
            d.line((x+1,23,x+1,30),fill=2)
        d.line((52,54,48,63),fill=1,width=3)
        d.rounded_rectangle((48,41,56,54),radius=3,fill=1)
        d.line((50,44,54,44),fill=2);d.line((50,47,54,47),fill=2)
    return im


def character(host,frame):
    """16x24, but curved heads, tapered torsos and separated elbows/feet."""
    im=Image.new('L',(16,24));d=ImageDraw.Draw(im)
    # Asymmetric arms swing without changing the familiar collision footprint.
    d.line((4,14,2,16+frame,2,18+frame),fill=2,width=2)
    d.line((11,14,13,16-frame,14,17-frame),fill=2,width=2)
    d.polygon([(5,12),(10,12),(12,15),(11,19),(4,19),(3,15)],fill=3)
    d.line((5,19,5-frame,22),fill=1,width=2)
    d.line((10,19,10+frame,22-frame),fill=1,width=2)
    d.line((3-frame,23,5-frame,23),fill=3);d.line((10+frame,23-frame,12+frame,23-frame),fill=3)
    if host==1:
        d.polygon([(4,2),(7,0),(11,1),(13,4),(12,8),(14,12),(12,16),(13,19),(10,18),(10,11),(4,11),(4,17),(2,18),(1,15),(3,11),(2,7),(2,4)],fill=1)
    d.ellipse((3,3,12,12),fill=2)
    if host==0:
        d.polygon([(2,6),(2,3),(4,1),(9,0),(12,2),(13,5),(11,5),(10,3),(7,4),(4,4),(4,6)],fill=1)
        d.line((4,2,7,1),fill=3)
        d.line((3,6,6,6,6,8,3,8,3,6),fill=3);d.line((9,6,12,6,12,8,9,8,9,6),fill=3)
        d.point((5,7),fill=1);d.point((10,7),fill=1);d.point((7,7),fill=1)
        d.line((5,10,10,10),fill=1);d.point((4,11),fill=1);d.point((11,11),fill=1)
        d.line((5,13,7,15,10,13),fill=1);d.line((7,16,7,19),fill=2)
    elif host==1:
        d.polygon([(3,6),(3,3),(6,2),(9,2),(6,4),(4,8)],fill=1)
        d.line((3,4,5,2,8,1),fill=3)
        d.line((11,4,12,8,11,11),fill=1)
        d.point((5,7),fill=1);d.point((10,7),fill=1)
        d.line((6,10,9,10),fill=3);d.line((6,13,9,13),fill=2)
    else:
        d.polygon([(2,6),(1,4),(3,2),(6,0),(10,0),(13,2),(14,4),(13,6),(11,5),(10,3),(7,4),(4,4),(4,6)],fill=1)
        d.point((5,2),fill=3)
        d.line((2,6,6,6,6,8,2,8,2,6),fill=1);d.line((9,6,13,6,13,8,9,8,9,6),fill=1)
        d.point((7,7),fill=1);d.point((4,7),fill=1);d.point((11,7),fill=1)
        d.polygon([(3,9),(5,10),(7,9),(9,9),(11,10),(12,9),(11,12),(9,14),(6,14),(4,12)],fill=1)
        d.line((6,11,9,11),fill=2)
    return im


def performer(pose):
    """24x40 Estefania: long parted hair, smiling face and denim jacket/jeans.
    Top two sprite rows use skin/white; lower rows use skin/denim blue.
    """
    im=Image.new('L',(24,40));d=ImageDraw.Draw(im)
    d.polygon([(4,8),(5,3),(9,0),(15,0),(19,3),(20,9),(19,16),(21,23),(19,30),(4,30),(3,24),(4,18),(3,13)],fill=1)
    d.polygon([(8,4),(12,3),(16,5),(18,9),(17,14),(14,18),(11,18),(8,16),(6,12),(6,8)],fill=2)
    d.polygon([(5,10),(5,5),(9,2),(12,1),(10,5),(8,7),(7,11)],fill=1)
    d.polygon([(12,1),(17,3),(19,7),(18,13),(16,7),(13,4)],fill=1)
    d.line((8,8,10,8),fill=1);d.line((14,8,16,9),fill=1)
    d.point((9,10),fill=1);d.point((15,10),fill=1)
    d.point((12,12),fill=1)
    d.line((9,14,15,14),fill=1);d.line((10,14,14,14),fill=3)
    d.line((11,16,14,16),fill=1)
    d.rectangle((10,18,14,21),fill=2)
    d.polygon([(7,20),(10,21),(12,23),(15,20),(18,22),(18,30),(6,30),(6,23)],fill=3)
    d.polygon([(10,22),(12,24),(14,22),(15,31),(9,31)],fill=1)
    d.line((8,22,10,25,8,27),fill=1);d.line((16,22,14,25,16,27),fill=1)
    arms=[((7,22,3,26,1,23),(17,22,21,25,22,21)),((7,22,2,16,2,11),(17,22,22,16,22,11)),((7,22,3,24,1,20),(17,22,21,16,18,13)),((7,22,3,16,6,13),(17,22,21,25,23,21))]
    for a in arms[pose]:
        # Sleeves end at the elbow, with exposed hands.
        d.line(a[:4],fill=3 if min(a[1],a[3])>=16 else 1,width=2)
        d.line(a[2:],fill=2,width=2)
    d.line((5,15,6,21,5,27),fill=1,width=2)
    d.line((18,15,17,22,19,27),fill=1,width=2)
    dx=1 if pose==2 else -1 if pose==3 else 0
    d.line((9,31,8+dx,37),fill=3,width=3);d.line((15,31,16+dx,37),fill=3,width=3)
    d.line((5+dx,39,9+dx,39),fill=1,width=2);d.line((15+dx,39,19+dx,39),fill=1,width=2)
    return im


def repairer(frame):
    """24x32 Chucho, four walk/facing frames, with the original foot anchor."""
    if frame>=2:return repairer(frame-2).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    im=Image.new('L',(24,32));d=ImageDraw.Draw(im)
    d.line((7,21,4,24+frame,3,26+frame),fill=2,width=2)
    d.line((16,21,19,23-frame,21,24-frame),fill=2,width=2)
    d.polygon([(8,18),(15,18),(18,21),(17,26),(6,26),(5,22)],fill=3)
    d.line((8,19,11,22,15,19),fill=1);d.line((11,23,11,26),fill=2)
    d.line((8,26,7-frame,30),fill=1,width=3)
    d.line((15,26,16+frame,29-frame),fill=1,width=3)
    d.line((4-frame,31,8-frame,31),fill=3)
    d.line((15+frame,30-frame,19+frame,30-frame),fill=3)
    d.ellipse((5,3,18,18),fill=2)
    d.ellipse((3,9,6,13),fill=2);d.ellipse((17,9,20,13),fill=2)
    d.polygon([(4,9),(3,5),(6,1),(13,0),(17,2),(19,5),(19,9),(17,8),(16,5),(11,5),(8,6),(6,5),(6,9)],fill=1)
    d.line((6,3,10,2,14,2),fill=3)
    d.ellipse((4,8,10,12),outline=3);d.ellipse((13,8,19,12),outline=3)
    d.line((10,9,13,9),fill=1);d.point((7,10),fill=1);d.point((16,10),fill=1)
    d.line((11,11,11,13),fill=3)
    d.polygon([(7,14),(10,13),(12,14),(14,13),(17,14),(17,15),(13,15),(11,15),(7,15),(6,16)],fill=1)
    d.line((9,17,14,17),fill=1)
    return im


def plaza_person(kind):
    """Dedicated 16x24 search portraits, independent of the other host sprites.

    Types keep the same hair/beard combinations as the magnifier. A broad head,
    cream tee and denim trousers retain Daniel's photo likeness at NES scale.
    """
    im=Image.new('L',(16,24));d=ImageDraw.Draw(im)
    top,bottom=[(2,2),(0,0),(1,1),(2,0),(0,2),(1,0)][kind]
    # Separate shoes, trouser legs, a curved shirt and bent elbows.
    d.line((5,19,5,22),fill=3,width=2);d.line((10,19,10,22),fill=3,width=2)
    d.line((3,23,6,23),fill=1);d.line((9,23,12,23),fill=1)
    d.polygon([(4,14),(11,14),(13,17),(11,20),(4,20),(2,17)],fill=2,outline=1)
    d.line((3,16,1,18,2,19),fill=2);d.line((12,16,14,18,13,19),fill=2)
    d.line((4,16,4,19),fill=3);d.line((11,16,11,19),fill=3)
    d.ellipse((2,2,13,14),fill=2,outline=1)
    if top==2:
        d.polygon([(1,7),(0,4),(2,2),(6,0),(10,0),(13,2),(15,5),(13,7),(12,4),(9,3),(6,5),(3,4),(3,7)],fill=1)
        d.line((3,2,7,1,10,1),fill=3)
        d.rectangle((2,6,6,9),outline=1);d.rectangle((9,6,13,9),outline=1)
        d.line((6,7,9,7),fill=1);d.point((4,8),fill=1);d.point((11,8),fill=1)
    elif top==0:
        d.polygon([(2,6),(1,4),(3,1),(10,0),(13,2),(14,5),(12,5),(11,3),(6,4),(3,4),(3,6)],fill=1)
        d.ellipse((2,6,6,9),outline=3);d.ellipse((9,6,13,9),outline=3)
        d.point((4,8),fill=1);d.point((11,8),fill=1);d.point((7,7),fill=1)
    else:
        d.polygon([(1,10),(1,4),(4,1),(9,0),(13,2),(15,7),(14,14),(15,19),(11,19),(12,12),(12,5),(8,3),(5,5),(3,10),(4,19),(1,18)],fill=1)
        d.point((5,8),fill=1);d.point((10,8),fill=1)
    d.point((7,10),fill=3)
    if bottom==2:
        d.polygon([(2,10),(5,11),(7,10),(9,10),(11,11),(13,10),(12,14),(9,16),(6,16),(3,14)],fill=1)
        d.line((5,12,10,12),fill=2);d.line((6,14,9,14),fill=3)
    elif bottom==0:
        d.line((5,11,10,11),fill=1);d.line((6,13,9,13),fill=1)
    else:
        d.line((5,12,10,12),fill=1);d.line((6,13,9,13),fill=2)
        d.line((5,16,6,19),fill=3);d.line((10,16,10,19),fill=3)
    return im


def menu_portrait(host,blink=False,gear=True):
    """64x64 menu likenesses from the user's group photo and Estefania's outdoor portrait.

    Face tiles end at y=47; clothing below uses a host-specific MMC5 palette.
    Gameplay and magnifier artwork intentionally keep their own drawing functions.
    """
    im=Image.new('L',(64,64));d=ImageDraw.Draw(im)
    d.ellipse((4,3,59,62),fill=2)
    if host==0:
        # Chucho: short side-swept hair, wire glasses, moustache and green tee.
        d.polygon([(5,63),(9,54),(22,48),(41,48),(54,55),(59,63)],fill=2)
        d.line((11,56,9,63),fill=1);d.line((50,55,54,63),fill=1)
        d.polygon([(25,42),(39,42),(40,48),(35,52),(29,51),(24,48)],fill=2)
        d.arc((22,43,43,56),5,175,fill=1,width=2)
        d.line((20,54,23,61),fill=3);d.line((44,54,42,61),fill=3)
        d.polygon([(20,10),(29,7),(39,9),(45,17),(46,29),(43,38),(38,44),(32,46),(25,43),(20,38),(17,28),(17,18)],fill=3)
        d.ellipse((14,23,20,32),fill=3);d.ellipse((43,22,49,31),fill=2)
        d.polygon([(42,16),(45,22),(44,34),(40,41),(33,45),(29,44),(37,41),(41,35)],fill=2)
        d.polygon([(16,24),(14,17),(15,10),(20,5),(30,3),(41,5),(47,11),(47,21),(44,24),(43,15),(40,11),(34,10),(27,13),(21,13),(20,22)],fill=1)
        d.line((19,10,26,7,36,7,42,10),fill=2)
        d.line((23,11,30,9,38,9),fill=2)
        d.line((20,19,26,18),fill=1);d.line((35,18,41,19),fill=1)
        d.ellipse((17,20,29,29),outline=1);d.ellipse((33,20,45,29),outline=1)
        d.line((29,23,33,23),fill=1);d.line((14,23,17,23),fill=1)
        d.point((23,25),fill=1);d.point((39,25),fill=1)
        d.line((31,24,30,30,33,31),fill=2)
        d.polygon([(23,34),(26,32),(30,32),(32,33),(35,32),(39,33),(42,35),(37,35),(33,34),(30,34),(26,35),(23,35)],fill=1)
        d.arc((25,32,39,40),0,180,fill=1)
        d.line((27,37,36,37),fill=3);d.line((30,41,35,41),fill=2)
        eyes=[(23,25),(39,25)]
    elif host==1:
        # Outdoor reference: side-swept hair, a slight three-quarter turn,
        # relaxed almond eyes and an open smile above a black leather jacket.
        d.polygon([(10,22),(13,12),(20,6),(30,3),(40,4),(47,9),(50,18),(49,32),(51,43),(49,54),(53,63),(5,63),(7,52),(9,42),(8,32)],fill=1)
        d.polygon([(5,63),(9,54),(23,48),(41,48),(55,54),(60,63)],fill=1)
        d.polygon([(26,40),(39,39),(40,45),(36,47),(29,47),(25,45)],fill=2)
        # A longer neck and rounded smiling cheeks keep adult proportions.
        d.polygon([(26,13),(34,10),(40,12),(44,18),(46,26),(45,31),(42,37),(38,41),(33,44),(28,43),(23,39),(20,33),(19,26),(21,19)],fill=3)
        d.ellipse((17,25,22,32),fill=2)
        d.polygon([(44,22),(46,27),(43,34),(40,39),(34,43),(30,42),(36,40),(40,35),(42,29)],fill=2)
        # The part sits to her left; the long sweep falls over the other shoulder.
        d.polygon([(17,31),(14,25),(15,18),(19,11),(26,6),(34,4),(41,6),(40,10),(35,10),(29,13),(26,17),(22,20),(21,28)],fill=1)
        d.polygon([(41,6),(46,10),(48,17),(48,25),(45,31),(43,27),(43,20),(41,15),(38,11)],fill=1)
        d.line((18,19,22,14,29,10,36,8),fill=2)
        d.line((44,16,45,21,45,25),fill=2)
        # Low, soft brows and small pupils avoid the startled, round-eyed look.
        d.line((22,21,25,20,28,20,30,21),fill=1)
        d.line((36,20,38,19,40,19,42,20),fill=1)
        if blink:
            d.line((23,25,25,26,28,26,30,24),fill=1)
            d.line((36,24,38,25,40,25,42,23),fill=1)
        else:
            d.line((23,25,25,23,27,23,30,25),fill=1)
            d.line((27,24,27,25),fill=1)
            d.line((25,27,28,27),fill=2)
            d.line((36,24,38,22,40,23,42,24),fill=1)
            d.line((39,23,39,24),fill=1)
            d.line((37,26,40,26),fill=2)
        d.line((34,25,34,28,36,30,33,31),fill=2)
        d.point((35,30),fill=1)
        # A visible upper row of teeth follows the lifted right corner.
        d.polygon([(26,34),(29,32),(33,33),(39,31),(42,33),(40,36),(36,39),(31,39),(28,37)],fill=1)
        d.polygon([(27,34),(32,34),(39,32),(40,33),(38,35),(33,36),(29,35)],fill=3)
        d.line((31,38,35,38,38,36),fill=2)
        d.line((24,32,23,34),fill=2);d.line((42,31,43,33),fill=2)
        d.line((29,41,33,42,36,41),fill=2)
        # Small hoops and the long, smooth sweep seen in the reference.
        d.arc((18,31,22,37),30,330,fill=2)
        d.point((19,34),fill=3)
        d.arc((43,31,46,36),0,270,fill=2)
        d.polygon([(12,32),(18,31),(18,40),(16,47),(13,52),(8,56),(4,57),(10,50),(11,43)],fill=1)
        d.line((15,38,14,44,11,50,7,54),fill=2)
        d.polygon([(45,37),(49,34),(48,44),(51,50),(48,54),(44,49),(43,44)],fill=1)
        # Black leather, gray lapel folds, silver snaps and a diagonal zip.
        # All jacket detail stays below the skin palette's y=48 boundary.
        d.line((18,51,23,49,28,53,23,57,28,63),fill=2)
        d.line((40,49,35,54,39,57,34,63),fill=2)
        d.line((23,58,27,63),fill=3)
        d.line((39,58,36,63),fill=3)
        d.point((23,52),fill=3);d.point((40,52),fill=3)
        d.line((12,55,9,62),fill=2);d.line((51,55,55,62),fill=2)
        eyes=[] # The eye shapes above include their own complete blink frame.
    else:
        # Daniel: fuller side-swept hair, heavier glasses, broad beard, white tee.
        d.polygon([(3,63),(7,54),(20,47),(41,47),(56,54),(61,63)],fill=3)
        d.polygon([(25,43),(39,42),(40,49),(34,53),(28,52),(24,49)],fill=2)
        d.arc((22,43,43,56),0,180,fill=1,width=2)
        d.line((11,55,9,62),fill=2);d.line((51,55,55,63),fill=2)
        d.polygon([(20,11),(30,8),(40,11),(46,18),(47,30),(44,39),(38,44),(30,45),(23,42),(18,34),(16,24)],fill=3)
        d.ellipse((13,23,20,32),fill=2);d.ellipse((44,23,50,32),fill=2)
        d.polygon([(15,26),(12,20),(12,13),(16,7),(23,4),(33,2),(43,5),(49,10),(51,18),(48,26),(45,23),(44,16),(40,12),(35,12),(28,17),(21,17),(20,25)],fill=1)
        d.line((17,14,21,9,28,7,38,7,44,10),fill=2)
        d.line((19,15,26,11,34,9),fill=2)
        d.line((19,19,27,18),fill=1);d.line((35,18,43,20),fill=1)
        d.rounded_rectangle((16,20,29,30),radius=2,outline=1,width=2)
        d.rounded_rectangle((33,20,47,30),radius=2,outline=1,width=2)
        d.line((29,24,33,24),fill=1,width=2)
        d.point((23,25),fill=1);d.point((39,25),fill=1)
        d.line((31,26,30,31,33,32),fill=2)
        d.polygon([(17,29),(21,32),(25,32),(28,31),(32,33),(36,31),(40,32),(45,30),(48,28),(47,36),(44,42),(38,47),(29,48),(23,44),(19,38)],fill=1)
        d.line((24,36,28,37,35,37,40,34),fill=3,width=2)
        d.line((28,40,35,40),fill=2)
        d.line((22,38,25,42),fill=2);d.line((40,40,37,44),fill=2)
        eyes=[(23,25),(39,25)]
    if blink:
        for x,y in eyes:
            d.point((x,y),fill=3)
            d.line((x-2,y+1,x+1,y+1),fill=1)
    if gear:
        d.arc((10,0,54,40),187,353,fill=1,width=3)
        d.arc((11,1,53,39),195,342,fill=2)
        for x in (9,49):
            d.rounded_rectangle((x,21,x+6,35),radius=2,fill=1)
            d.line((x+1,24,x+1,31),fill=2)
        d.line((52,53,48,63),fill=1,width=3)
        d.rounded_rectangle((48,42,56,55),radius=3,fill=1)
        d.line((50,45,54,45),fill=2);d.line((50,48,54,48),fill=2)
    return im
