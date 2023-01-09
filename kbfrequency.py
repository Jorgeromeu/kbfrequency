from collections import defaultdict

import cmasher as cmr
from lxml import etree

def set_style(svg, color):
    if svg.attrib.get('style'):
        svg.attrib['style'] = svg.attrib['style'].replace('fill:#ffffff', f'fill:{color}')

def write_to_svg(frequencies: dict, blankfile, outfile, colorbar='viridis'):
    """
    Create heatmap svg
    @param frequencies key frequency dictionary
    """

    # create colormap
    max_freq = max(frequencies.values())
    cmap = list(cmr.take_cmap_colors(colorbar, max_freq + 1, return_fmt='hex'))

    # parse svg's xml
    root = etree.parse(open(blankfile, 'rb'))

    for el in root.iter():

        keycode = el.get('kcode')
        color = cmap[frequencies[keycode]]
        set_style(el, color)

    f = open(outfile, 'wb')
    f.write(etree.tostring(root))
    f.close()

def parse_frequencies(logfile: str):
    frequencies = defaultdict(lambda: 0)
    for line in open(logfile):

        if line[0] == '-':
            # special case of '-'
            name = '-'
            num = line[2:]
        else:
            name, num = line.split('-')

        # for shift, append the num to keycode
        if name == 'shift' or name == 'ctrl':
            name += num

        frequencies[name] += 1

    return frequencies

if __name__ == '__main__':

    datafiles = ['keys.txt']

    freq = parse_frequencies(datafiles[0])

    write_to_svg(freq, 'blank.svg', 'out.svg')
