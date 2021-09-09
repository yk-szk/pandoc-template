#!/usr/bin/env python3
'''
Pandoc filter that replaces image formats
'''
import argparse
import sys
from pathlib import Path
import panflute as pf


def svg2png(input_filename, output_filename):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    drawing = svg2rlg(input_filename)
    renderPM.drawToFile(drawing, output_filename, fmt="PNG")


def svg2pdf(input_filename, output_filename):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    print('Convert', input_filename, output_filename, file=sys.stderr)
    drawing = svg2rlg(str(input_filename))
    renderPDF.drawToFile(drawing, str(output_filename))


def main():
    parser = argparse.ArgumentParser(
        description='Pandoc filter for replacing image formats.')
    parser.add_argument('target', help='Target format', nargs='?')
    parser.add_argument(
        '--pairs',
        help="Replacement pairs (comma separated). default:%(default)s")
    parser.add_argument(
        '--convs',
        help="Conversion pairs (comma separated). default:%(default)s",
        default='')
    parser.add_argument('-v', '--verbose', help="Verbose", action='store_true')
    args = parser.parse_args()

    if args.pairs is None:
        if args.target == 'latex':
            args.pairs = 'svg2pdf'
        elif args.target == 'html':
            args.pairs = 'png2svg'
        elif args.target == 'docx':
            args.pairs = 'png2emf,svg2emf'
        else:
            args.pairs = ''

    pairs = [['.{}'.format(ext) for ext in e.split('2')]
             for e in args.pairs.split(',')]
    convs = [[
        '.{}'.format(ext) for ext in e.split('2')
    ] for e in (args.convs.split(',') if args.convs else args.pairs.split(','))
             ]

    def action(elem, doc):
        if isinstance(elem, pf.Image):
            p = Path(elem.url)
            for pair in pairs:
                if p.suffix == pair[0]:
                    p_original = p
                    p = p.with_suffix(pair[1])
                    if p.exists():
                        elem.url = str(p)
                    else:
                        for conv in convs:
                            if conv[0] == pair[0] == '.svg' and conv[
                                    1] == pair[1] == '.pdf':
                                svg2pdf(p_original, p)
                                elem.url = str(p)
                                break
                        else:
                            if True:
                                print('{} not found ({} to {}).'.format(
                                    p_original, pair[0], pair[1]),
                                      file=sys.stderr)
        return elem

    pf.run_filter(action)
    return 0


if __name__ == "__main__":
    sys.exit(main())
