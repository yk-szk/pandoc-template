import os
import sys
import argparse
from shutil import which
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description='Convert svg to other image formats using inkscape.')
    parser.add_argument('input', help='Input directory', metavar='<input>')
    parser.add_argument('output', help='Output directory', metavar='<output>')
    parser.add_argument('--inkscape',
                        help='Inkscape binary path. default: %(default)s',
                        metavar='<path>',
                        default=r'C:\Program Files\Inkscape\bin\inkscape.com'
                        if os.name == 'nt' else 'inkscape')
    parser.add_argument('--ext',
                        help='Output file extension. default: %(default)s',
                        metavar='<ext>',
                        default='.pdf')

    args = parser.parse_args()

    if args.input == args.output:
        print('Intput directory cant be output directory')
        return 1

    # check inkscape existance
    if which(args.inkscape) is None:
        print('{} not found.')
        return 1

    indir = Path(args.input)
    outdir = Path(args.output)
    for fn in indir.glob('*.svg'):
        outname = outdir / fn.name
        outname = outname.with_suffix(args.ext)
        conv_args = [args.inkscape, str(fn)]
        if args.ext == '.svg':
            conv_args.append('-l')
        conv_args.append('--export-filename={}'.format(outname))
        print(outname)
        subprocess.check_call(conv_args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
