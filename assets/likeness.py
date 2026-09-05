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
