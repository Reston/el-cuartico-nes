"""Gameplay actors drawn on their native 16 x 32 grid (no portrait resizing).

Each actor has a 2 KiB page: 16 poses x eight NES tiles. The upper 16 pixels
use the shared face palette; the torso and trousers use separate palettes.
Pose order is mirrored by the animation state selector in adventure.c.
"""
from PIL import Image, ImageDraw

POSES = ('idle', 'blink', 'run-contact-a', 'run-down-a', 'run-pass-a',
         'run-contact-b', 'run-down-b', 'run-pass-b', 'rise', 'apex',
         'fall', 'land', 'anticipate', 'action', 'recover', 'hurt')

# Three-quarter faces look toward the action, with a proper nose silhouette.
# 1: dark hair/outline, 2: skin, 3: light lenses/highlight. Zero is transparent.
HEADS = (
    (
        '0000111111100000',
        '0001112111110000',
        '0011121111111000',
        '0011112222221000',
        '0011222222221000',
        '0011221112111100',
        '0011213231323100',
        '0011221112111220',
        '0001222222222200',
        '0001222111121000',
        '0000122233321000',
        '0000012222210000',
        '0000001221100000',
    ),
    (
        '0000011111100000',
        '0000112211110000',
        '0001122111111000',
        '0011122222211000',
        '0011222222221000',
        '0011222122121000',
        '0011222322321000',
        '0011222222222200',
        '0011222222222000',
        '0011122223321000',
        '0011122233221000',
        '0011112222210000',
        '0011111221100000',
    ),
    (
        '0001111111100000',
        '0011121111110000',
        '0111211111111000',
        '0111122222211000',
        '0111222222221000',
        '0011211112111100',
        '0011213312133100',
        '0011211112111220',
        '0001122222221100',
        '0001111222211000',
        '0001111333311000',
        '0000111121110000',
        '0000011111100000',
    ),
)

# (rear knee, rear ankle, front knee, front ankle, body bob)
RUN = (
    ((4, 26), (1, 29), (11, 26), (13, 30), 0),
    ((5, 26), (4, 28), (11, 27), (11, 30), 1),
    ((10, 25), (12, 27), (8, 27), (7, 30), 0),
    ((11, 26), (13, 29), (5, 27), (2, 30), 0),
    ((11, 26), (11, 28), (6, 27), (4, 30), 1),
    ((6, 25), (3, 27), (9, 27), (10, 30), 0),
)


def actor_frame(who, pose):
    im = Image.new('L', (16, 32)); d = ImageDraw.Draw(im)
    bob = RUN[pose - 2][4] if 2 <= pose <= 7 else (2 if pose == 11 else 0)
    # Legs have a continuous thigh/calf silhouette, not disconnected sticks.
    if 2 <= pose <= 7:
        rk, ra, fk, fa, _ = RUN[pose - 2]
    elif pose == 8:
        rk, ra, fk, fa = (4, 25), (2, 27), (11, 24), (12, 27)
    elif pose == 9:
        rk, ra, fk, fa = (4, 25), (3, 28), (11, 25), (13, 28)
    elif pose == 10:
        rk, ra, fk, fa = (5, 26), (4, 30), (11, 26), (12, 30)
    elif pose == 11:
        rk, ra, fk, fa = (3, 27), (4, 30), (12, 27), (12, 30)
    elif pose in (12, 13, 14):
        rk, ra, fk, fa = (5, 27), (3, 30), (11, 27), (12, 30)
    elif pose == 15:
        rk, ra, fk, fa = (4, 25), (1, 27), (11, 27), (12, 30)
    else:
        rk, ra, fk, fa = (6, 27), (5, 30), (10, 27), (10, 30)
    for hip,knee,ankle in (((6,22+bob),rk,ra),((10,22+bob),fk,fa)):
        d.line((hip,knee,ankle),fill=1,width=4)
        d.line((hip,knee,ankle),fill=3,width=2)
        ax,ay=ankle
        d.line((max(0,ax-1),ay+1,min(15,ax+3),ay+1),fill=3,width=1)
        d.point((min(15,ax+3),ay),fill=2)
    # Hair behind the jacket follows the stride, not a fixed portrait cutout.
    if who==1:
        sway = -1 if pose in (2,3,8,13) else 0
        d.polygon([(3,8+bob),(6,9+bob),(6,19+bob),(3+sway,22+bob),(1+sway,19+bob)],fill=1)
        d.line((2,12+bob,2+sway,18+bob),fill=2)
    # Neck and torso. Chucho's shirt, Estefania's open jacket, Daniel's tee.
    d.rectangle((6,12+bob,10,16+bob),fill=2)
    d.polygon([(4,15+bob),(7,14+bob),(11,15+bob),(13,19+bob),(11,23+bob),(5,23+bob),(3,19+bob)],fill=1)
    d.polygon([(5,16+bob),(7,15+bob),(10,16+bob),(11,22+bob),(5,22+bob)],fill=3)
    if who==1:
        d.line((7,16+bob,8,22+bob),fill=1,width=2)
        d.point((5,18+bob),fill=2)
    elif who==2:
        d.line((7,15+bob,9,16+bob,10,15+bob),fill=1)
    else:
        d.line((5,21+bob,10,21+bob),fill=1)
    # Counter-swinging arms: hands follow elbows through contact and passing.
    rear=((3,19+bob),(4,22+bob));front=((12,20+bob),(11,23+bob))
    if 2<=pose<=7:
        arm=(pose-2)%6
        rear=[((3,18),(1,17)),((3,19),(2,20)),((4,20),(5,22)),((4,21),(6,23)),((3,20),(3,22)),((3,19),(1,19))][arm]
        front=[((13,21),(11,24)),((13,20),(13,22)),((12,18),(14,17)),((12,17),(14,16)),((13,18),(14,19)),((12,20),(12,23))][arm]
    elif pose==8:rear=((2,18),(1,15));front=((12,15),(13,12))
    elif pose==9:rear=((2,18),(1,16));front=((13,17),(14,15))
    elif pose==10:rear=((2,19),(1,17));front=((13,18),(14,16))
    elif pose==11:rear=((3,22),(4,25));front=((12,22),(13,25))
    elif pose==12:rear=((3,19),(2,17));front=((10,19),(8,17))
    elif pose==13:
        rear=((4,20),(6,21));front=((13,18),(15,18)) if who!=2 else ((12,18),(13,15))
    elif pose==14:front=((12,19),(13,21))
    elif pose==15:rear=((2,16),(1,13));front=((12,16),(14,13))
    for shoulder,(elbow,hand) in (((4,16+bob),rear),((10,16+bob),front)):
        d.line((shoulder,elbow,hand),fill=1,width=4)
        d.line((shoulder,elbow),fill=3,width=2)
        d.line((elbow,hand),fill=2,width=2)
    # Draw the readable face last; head occupies under half of the height.
    head=Image.new('L',(16,13))
    head.putdata([int(c) for row in HEADS[who] for c in row])
    if pose==1:
        hd=ImageDraw.Draw(head)
        hd.line((7,6,8,6),fill=1);hd.line((11,6,12,6),fill=1)
    if pose==15:
        hd=ImageDraw.Draw(head)
        hd.line((7,6,8,7),fill=1);hd.line((11,6,12,7),fill=1)
    im.paste(head,(0,1+bob),head.point(lambda v:255 if v else 0))
    return im


def actor_tiles(who, pack):
    tiles=[]
    for pose in range(16):
        im=actor_frame(who,pose)
        for y in range(0,32,8):
            for x in (0,8):tiles.append(pack(im.crop((x,y,x+8,y+8))))
    assert len(tiles)==128
    return tiles


def action_tiles(pack):
    tiles=[]
    # Each action is one sprite wide, retaining room for enemies on a scanline.
    for who in range(3):
        im=Image.new('L',(8,16));d=ImageDraw.Draw(im)
        if who==0:  # glove and a short impact arc extend the actual fist
            d.line((0,7,4,7),fill=2,width=3)
            d.rectangle((3,4,6,8),fill=2,outline=3)
            d.line((5,1,7,3,7,10,5,12),fill=3)
        elif who==1:  # microphone muzzle, visibly aligned with the shot
            d.rectangle((0,6,4,8),fill=1)
            d.ellipse((2,3,6,7),fill=3)
            d.line((5,0,5,2),fill=3);d.line((7,5,7,7),fill=2)
        else:  # Daniel braces a bright, compact shield in front of his body
            d.polygon([(1,2),(6,1),(7,10),(4,14),(1,10)],fill=3)
            d.polygon([(2,4),(5,3),(6,9),(4,11),(2,9)],fill=1)
            d.line((4,5,3,7,5,8,4,10),fill=2)
        for y in (0,8):tiles.append(pack(im.crop((0,y,8,y+8))))
    return tiles
