"""Native NES adventure tiles; generated locally, without external images/audio."""
from PIL import Image, ImageDraw
from likeness import character, bust
from ui_font import draw_ui_glyph


def build_adventure(root, font, text, pack):
    def tile_bank():
        tiles = [bytes(16) for _ in range(256)]
        for ch in font:
            if ord(ch) < 128:
                im = Image.new('L', (8, 8))
                draw_ui_glyph(im, ch, 3, text)
                tiles[ord(ch)] = pack(im)
        return tiles

    def put(tiles, first, im):
        for y in range(0, im.height, 8):
            for x in range(0, im.width, 8):
                tiles[first] = pack(im.crop((x, y, x + 8, y + 8)))
                first += 1

    def food_icons(tiles, first):
        for kind in range(3):
            im = Image.new('L', (16, 16)); d = ImageDraw.Draw(im)
            if kind == 0:
                d.polygon([(6,1),(10,1),(14,9),(13,13),(8,15),(3,13),(2,9)], fill=2, outline=3)
                d.ellipse((5,7,10,12), fill=1)
            elif kind == 1:
                d.polygon([(2,4),(13,4),(14,8),(8,15),(1,8)], fill=2, outline=3)
                d.polygon([(3,1),(8,3),(13,1),(10,5),(6,5)], fill=3)
                for x,y in ((4,7),(9,7),(6,10),(10,10)): d.point((x,y),fill=1)
            else:
                d.ellipse((5,0,11,13), fill=3)
                for y in (3,6,9):d.line((6,y,10,y),fill=1)
                d.line((8,1,8,11),fill=1)
                d.polygon([(1,7),(8,13),(14,5),(12,13),(8,15),(3,13)],fill=2)
            put(tiles, first+kind*4, im)

    banks = []
    for world in range(5):
        tiles = tile_bank()
        # Platform tops, faces and decorative trim share collision silhouettes.
        im = Image.new('L', (32, 16)); d = ImageDraw.Draw(im)
        d.rectangle((0, 1, 31, 15), fill=1)
        d.line((0, 0, 31, 0), fill=3)
        d.line((0, 2, 31, 2), fill=2)
        for x in range(2, 32, 8):
            if world == 0:
                d.line((x, 4, x + 4, 7, x + 2, 12), fill=2)
            elif world in (1, 3):
                d.rectangle((x, 5, x + 4, 10), outline=2)
                d.point((x + 2, 7), fill=3)
            else:
                d.line((x, 5, x + 5, 5, x + 5, 11), fill=2)
        put(tiles, 128, im)
        # Stars, clouds, cables, vegetation and stonework are background only.
        for index in range(136, 192):
            im = Image.new('L', (8, 8)); d = ImageDraw.Draw(im)
            k = index - 136
            if k < 8:
                if world == 0:
                    d.polygon([(0, 7), (3 + k % 3, k % 4), (7, 7)], fill=1)
                    d.line((3 + k % 3, k % 4, 5, 5), fill=2)
                elif world == 1:
                    d.line((0, 2, 5, 2, 5, 7), fill=1)
                    d.point((5, 2), fill=2)
                elif world == 2:
                    d.line((4, 7, 4, 1), fill=1)
                    d.polygon([(0, 5), (4, 0), (7, 5)], fill=2)
                elif world == 3:
                    d.rectangle((1, 2, 6, 6), outline=1)
                    d.line((2, 3, 5, 3), fill=2)
                else:
                    d.line((0, 1, 7, 1, 7, 7), fill=1)
                    d.point((2, 4), fill=2)
            elif k < 16:
                d.ellipse((-3 + k % 3, 3, 10, 9), fill=1)
                d.line((1, 4, 5, 4), fill=2)
            elif k < 24:
                d.line((0, 7, 3, 1, 6, 7), fill=1)
                d.point((3, 1), fill=2)
            elif k < 32:
                d.rectangle((1, 1, 6, 7), fill=1)
                d.rectangle((2, 2, 4, 4), fill=2)
            else:
                d.point((k % 7, (k * 3) % 7), fill=1)
            tiles[index] = pack(im)
        im = Image.new('L', (32, 32)); d = ImageDraw.Draw(im)
        if world == 0:
            d.polygon([(0, 31), (15, 1), (31, 31)], fill=1)
            d.polygon([(15, 1), (8, 14), (14, 11), (18, 15), (23, 15)], fill=2)
            d.line((15, 2, 17, 13), fill=3)
        elif world == 1:
            d.rectangle((3, 4, 28, 31), fill=1, outline=2)
            d.rectangle((7, 8, 24, 19), fill=0, outline=2)
            for x in range(9, 24, 4): d.line((x, 10, x, 17), fill=2)
            d.ellipse((11, 24, 19, 31), fill=2)
        elif world == 2:
            d.polygon([(0, 31), (0, 18), (8, 11), (22, 11), (31, 18), (31, 31)], fill=1)
            d.polygon([(0, 18), (15, 4), (31, 18)], fill=2)
            d.rectangle((7, 21, 12, 28), fill=2); d.rectangle((21, 21, 26, 28), fill=2)
        elif world == 3:
            d.rectangle((0, 3, 31, 31), fill=1)
            for y in (5, 15, 25):
                d.line((0, y + 5, 31, y + 5), fill=2)
                for x in (3, 11, 21):d.rectangle((x, y, x + 5, y + 4), fill=2)
        else:
            d.rectangle((3, 10, 28, 31), fill=1)
            for x in (3, 13, 23):d.rectangle((x, 4, x + 5, 12), fill=1)
            d.arc((10, 14, 21, 29), 180, 360, fill=2)
            d.line((10, 21, 10, 31), fill=2);d.line((21, 21, 21, 31), fill=2)
        put(tiles, 136, im)
        im = Image.new('L', (32, 16));d = ImageDraw.Draw(im)
        if world in (0, 2):
            d.ellipse((0, 6, 19, 18), fill=1);d.ellipse((10, 0, 29, 17), fill=1)
            d.line((12, 2, 20, 2), fill=2)
        elif world == 1:
            d.rectangle((0, 7, 31, 12), fill=1, outline=2)
            for x in (7, 23):
                d.ellipse((x-5, 3, x+5, 13), fill=1, outline=2)
                d.line((x-3, 8, x+3, 8), fill=3);d.line((x, 5, x, 11), fill=3)
        elif world == 3:
            d.line((4, 0, 4, 3), fill=2);d.line((27, 0, 27, 3), fill=2)
            d.rectangle((0, 3, 31, 15), fill=1, outline=2)
            for k,ch in enumerate('CAJA'):
                glyph=Image.new('L',(8,8));draw_ui_glyph(glyph,ch,3,text);im.paste(glyph,(k*8,5))
        else:
            for x in (3,19):
                d.polygon([(x,0),(x+9,0),(x+9,11),(x+5,15),(x,11)], fill=1, outline=2)
                d.line((x+5,3,x+5,9), fill=3)
        put(tiles, 152, im)
        im = Image.new('L', (16, 32));d = ImageDraw.Draw(im)
        if world in (0, 2):
            d.rectangle((7, 13, 9, 31), fill=1)
            d.polygon([(0, 21), (8, 2), (15, 21)], fill=1)
            d.line((7, 7, 3, 18), fill=2)
        else:
            d.rectangle((5, 0, 10, 31), fill=1)
            d.line((6, 0, 6, 31), fill=2)
            for y in (3, 17):d.rectangle((3, y, 12, y + 3), fill=2)
        put(tiles, 160, im)
        im = Image.new('L', (16, 32)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, 15, 31), radius=3, fill=1, outline=2)
        d.rectangle((3, 4, 12, 30), fill=0)
        d.line((7, 12, 11, 16, 7, 20), fill=3, width=2)
        put(tiles, 192, im)
        # Closed clapboard / open passage, ladder and directional chevrons.
        im = Image.new('L', (16, 16)); d = ImageDraw.Draw(im)
        d.rectangle((1, 2, 14, 14), fill=1, outline=2)
        for x in (2, 6, 10): d.line((x, 2, x + 3, 5), fill=3)
        d.line((4, 9, 11, 9), fill=3)
        put(tiles, 200, im)
        im = Image.new('L', (8, 8)); d = ImageDraw.Draw(im)
        d.line((1, 0, 1, 7), fill=2); d.line((6, 0, 6, 7), fill=2)
        for y in (1, 5): d.line((1, y, 6, y), fill=3)
        tiles[204] = pack(im)
        im = Image.new('L', (8, 8)); d = ImageDraw.Draw(im)
        d.line((2, 1, 5, 4, 2, 7), fill=3, width=2); tiles[205] = pack(im)
        im = Image.new('L', (16, 8)); d = ImageDraw.Draw(im)
        d.rectangle((0, 3, 15, 7), fill=2); d.line((0, 2, 15, 2), fill=3)
        for x in (3, 11): d.line((x, 4, x + 2, 6), fill=1)
        put(tiles, 206, im)
        # Background relays avoid consuming the NES eight-sprite scanline budget.
        for phase in range(2):
            im=Image.new('L',(16,16));d=ImageDraw.Draw(im)
            d.line((8,0,8,4),fill=3);d.rectangle((2,4,13,15),fill=1,outline=2)
            d.rectangle((4,6,11,11),fill=0,outline=3 if not phase else 2)
            if phase:d.line((5,9,7,11,10,7),fill=3)
            else:
                d.line((5,7,10,10),fill=3);d.line((5,10,10,7),fill=3)
                d.point((0,2),fill=2);d.point((15,2),fill=2)
            put(tiles,208+phase*4,im)
        im=Image.new('L',(8,8));d=ImageDraw.Draw(im)
        d.line((0,0,2,0),fill=2);d.line((5,0,7,0),fill=2);tiles[216]=pack(im)
        food_icons(tiles,220)
        banks.append(b''.join(tiles))

    sprites = [bytes(16) for _ in range(256)]
    from adventure_actors import actor_tiles, action_tiles
    sprites[:128] = actor_tiles(0, pack)
    sprites[128:134] = action_tiles(pack)
    for index in range(144, 168):
        im = Image.new('L', (8, 8)); d = ImageDraw.Draw(im)
        if index in (152, 153):
            d.polygon([(0, 2), (2, 0), (4, 2), (6, 0), (7, 2), (7, 4), (4, 7), (0, 4)],
                      fill=3 if index == 152 else 1)
        elif index in (154, 155, 156, 157):
            d.rectangle((0, 0, 7, 7), fill=2, outline=3)
            d.rectangle((1, 2, 6, 4), fill=1)
            d.point((2, 3), fill=3);d.point((5, 3), fill=3)
        elif index == 158:
            d.rectangle((1, 1, 6, 7), fill=1, outline=3)
            d.line((3, 5, 6, 1), fill=2)
        elif index == 159:
            d.rectangle((2, 0, 5, 1), fill=3)
            d.rectangle((1, 2, 6, 7), fill=2, outline=3)
            d.line((3, 3, 3, 5), fill=1);d.line((2, 4, 4, 4), fill=1)
        elif index == 160:
            d.ellipse((1, 1, 6, 6), fill=3); d.point((3, 3), fill=2)
        elif index == 161:
            d.line((1, 5, 6, 5), fill=1)
        elif index == 162:
            d.line((1, 1, 4, 4, 1, 7), fill=3, width=2)
        elif index in (164, 165):
            d.rectangle((0, 2, 7, 6), fill=2)
            d.line((0, 1, 7, 1), fill=3)
            d.line((2, 3, 4, 5), fill=1)
        else:
            d.line((0, 4, 7, 4), fill=3)
            d.line((4, 0, 4, 7), fill=2)
        sprites[index] = pack(im)
    for enemy in range(6):
        for phase in range(2):
            im = Image.new('L', (16, 16)); d = ImageDraw.Draw(im)
            if enemy in (0, 3):
                d.rounded_rectangle((1, 3, 14, 12), radius=3, fill=2, outline=1)
                d.rectangle((4, 5, 11, 8), fill=1)
                d.point((5 + phase, 6), fill=3); d.point((10 + phase, 6), fill=3)
                d.line((2, 14, 5, 14 - phase), fill=3, width=2)
                d.line((10, 14 - phase, 13, 14), fill=3, width=2)
            elif enemy in (1, 4):
                d.polygon([(3, 5), (8, 5), (14, 1), (14, 13), (8, 9), (3, 9)], fill=2, outline=1)
                d.line((4, 10, 4, 14, 9, 14), fill=3, width=2)
                if phase: d.line((0, 2, 2, 3), fill=3)
            else:
                d.ellipse((3, 2, 12, 12), fill=2, outline=1)
                d.line((1, 1 if phase else 9, 4, 6, 11, 6, 15, 1 if phase else 9), fill=3)
                d.point((6, 5), fill=1); d.point((10, 5), fill=1)
            put(sprites, 168 + enemy * 8 + phase * 4, im)
    for phase in range(4):
        im = Image.new('L', (24, 24)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((3, 2, 20, 19), radius=4, fill=2, outline=1)
        d.rectangle((6, 5, 17, 10), fill=1)
        d.line((7, 7, 10, 7), fill=3); d.line((14, 7, 16, 7), fill=3)
        d.rectangle((8, 13, 15, 16), fill=3 if phase == 2 else 1)
        d.line((1, 10, 1, 16 - phase), fill=3, width=2)
        d.line((22, 10, 22, 16 - phase), fill=3, width=2)
        d.line((6, 20, 5 + (phase & 1), 23), fill=1, width=3)
        d.line((17, 20, 18 - (phase & 1), 23), fill=1, width=3)
        put(sprites, 216 + phase * 9, im)
    banks.append(b''.join(sprites))

    ui = tile_bank()
    for who in range(3):
        im = bust(who).resize((32, 32), Image.Resampling.NEAREST)
        put(ui, 128 + who * 16, im)
    # UI furniture and clapboard: reusable large shapes, not oversized text.
    im = Image.new('L', (64, 16)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 15), fill=1, outline=2)
    for x in range(0, 64, 12): d.polygon([(x, 0), (x + 6, 0), (x + 12, 7), (x + 6, 7)], fill=3)
    d.line((5, 11, 58, 11), fill=2)
    put(ui, 176, im)
    # Larger brand lettering is art; instructions retain the compact 8x8 grid.
    brand = Image.new('L', (88, 8)); text(brand, 0, 0, 'EL CUARTICO', 3)
    put(ui, 192, brand.resize((176, 16), Image.Resampling.NEAREST))
    line = Image.new('L', (8, 8)); ImageDraw.Draw(line).line((0, 4, 7, 4), fill=2)
    ui[238] = pack(line)
    food_icons(ui,240)
    banks.append(b''.join(ui))
    # Five final 1 KiB sprite pages reuse the enemy tiles and provide distinct bosses.
    tails = []
    for world in range(5):
        tiles = list(sprites[192:])
        for phase in range(4):
            im = Image.new('L', (24, 24)); d = ImageDraw.Draw(im)
            if world == 0:  # excessive rescue crane
                d.rectangle((3, 14, 21, 21), fill=2, outline=1)
                d.rectangle((13, 9, 20, 15), fill=2, outline=3)
                d.line((17, 11, 9, 2, 2, 2), fill=3, width=3)
                d.line((3, 3, 3, 9 + phase, 6, 11 + phase), fill=2, width=2)
                for x in (6, 18): d.ellipse((x-3, 19, x+3, 23), fill=1, outline=3)
            elif world == 1:  # loudspeaker that will not listen
                d.polygon([(2, 8), (10, 8), (21, 1), (21, 18), (10, 12), (2, 12)], fill=2, outline=3)
                d.rectangle((18, 4, 21, 15), fill=1)
                d.line((9, 13, 9, 21, 16, 21), fill=3, width=3)
                if phase == 2: d.line((0, 2, 6, 5), fill=3)
            elif world == 2:  # invitation guarded by an origami owl
                d.polygon([(3, 1), (8, 5), (16, 5), (21, 1), (20, 18), (12, 23), (4, 18)], fill=2, outline=1)
                for x in (5, 13):
                    d.ellipse((x, 6, x+6, 12), fill=3); d.point((x+3, 9), fill=1)
                d.polygon([(10, 13), (14, 13), (12, 17)], fill=1)
                d.line((2, 13, 0, 7 if phase == 2 else 19), fill=3, width=2)
                d.line((21, 13, 23, 7 if phase == 2 else 19), fill=3, width=2)
            elif world == 3:  # runaway checkout cart
                d.polygon([(2, 6), (21, 6), (18, 17), (5, 17)], fill=2, outline=3)
                for x in (7, 12, 17): d.line((x, 8, x, 15), fill=1)
                d.line((0, 2, 3, 2, 5, 19, 19, 19), fill=3, width=2)
                for x in (7, 18):d.ellipse((x-2, 20, x+2, 23), fill=1, outline=3)
            else:  # a nickname becomes a dragon
                d.polygon([(8, 8), (1, 2), (0, 17), (8, 14), (16, 14), (23, 17), (22, 2), (16, 8)], fill=2, outline=3)
                d.ellipse((7, 3, 17, 20), fill=2, outline=1)
                d.point((10, 8), fill=3);d.point((15, 8), fill=3)
                d.line((10, 13, 15, 13), fill=1)
                d.line((8, 20, 5, 23), fill=3, width=2);d.line((16, 20, 19, 23), fill=3, width=2)
            put(tiles, 24 + phase * 9, im.resize((16, 24), Image.Resampling.NEAREST))
        tails.append(b''.join(tiles))
    pages = b''.join(tails).ljust(8192, b'\0')
    banks.extend((pages[:4096], pages[4096:]))
    # Last previously unused 4 KiB: two 2 KiB actor pages. Actor 0 reuses
    # the old hero area in bank 59; shared props/enemies stay in its last half.
    banks.append(b''.join(actor_tiles(1, pack) + actor_tiles(2, pack)))
    assert len(banks) == 10 and all(len(b) == 4096 for b in banks)
    return banks
