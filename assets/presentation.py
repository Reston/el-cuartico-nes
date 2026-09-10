"""A native NES broadcast slate for help, pause and result screens."""
from PIL import Image, ImageDraw
from ui_font import draw_ui_glyph


def build_presentation(root, font, text, pack):
    im = Image.new('L', (256, 240))
    draw = ImageDraw.Draw(im)
    draw.rectangle((16, 8, 239, 231), outline=1)
    draw.line((24, 8, 231, 8), fill=2)
    draw.line((24, 231, 231, 231), fill=2)
    for x in (16, 239):
        draw.line((x, 16, x, 55), fill=2)
        draw.line((x, 208, x, 223), fill=2)
    text(im, 68, 24, 'el cuartico', 3, 2)
    text(im, 64, 48, 'ESTAMOS GRABANDO', 2)
    for y in (64, 192):
        draw.line((24, y, 231, y), fill=1)
        draw.line((24, y, 55, y), fill=2)
        draw.line((200, y, 231, y), fill=2)
    # Quiet VU bars flank the logo, keeping the content area entirely clear.
    for x, heights in ((32, (5, 11, 17)), (208, (17, 11, 5))):
        for i, height in enumerate(heights):
            draw.rectangle((x+i*4, 39-height, x+i*4+1, 39), fill=2)
    tiles = [bytes(16) for _ in range(128)]
    for ch in font:
        q = Image.new('L', (8, 8))
        draw_ui_glyph(q, ch, 3, text)
        tiles[ord(ch)] = pack(q)
    free = [i for i in range(1, 128) if chr(i) not in font and i != 32]
    ids = []
    for y in range(0, 240, 8):
        for x in range(0, 256, 8):
            tile = pack(im.crop((x, y, x+8, y+8)))
            if tile not in tiles:
                if free:
                    tiles[free.pop(0)] = tile
                else:
                    tiles.append(tile)
            ids.append(tiles.index(tile))
    assert len(tiles) <= 256
    root.joinpath('presentation.nam').write_bytes(bytes(ids+[0]*64))
    return b''.join(tiles)+bytes((256-len(tiles))*16), len(tiles)
