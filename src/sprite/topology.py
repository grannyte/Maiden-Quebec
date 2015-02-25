__author__ = 'plperron'


def build_temple(self, sprite_sheet):
    zone = [
        '###################',
        '#         ##### #T#',
        '#              D# #',
        '#         ##### # #',
        '#              D# #',
        '#         ##### # #',
        '#              D# #',
        '#         #####   #',
        '###################',
    ]
    topology = dict()
    topology['zone'] = zone
    topology['height'] = len(zone)
    topology['width'] = len(zone[0])
    topology['sprite_sheet'] = sprite_sheet
    topology['wall'] = '#'
    topology['door'] = 'D'
    topology['floor'] = ' '
    topology['chest'] = 'T'

def __search(zone, symbol):
    for y in range(0, len(zone)):
        for x in range(0, len(zone[y])):
            pass
