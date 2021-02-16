#!/usr/bin/env python3
import argparse
import sys
import panflute as pf


def main():
    parser = argparse.ArgumentParser(
        description='Remove header above specified level.')
    parser.add_argument('target', help='Target format', nargs='?')
    parser.add_argument('-l',
                        '--level',
                        help="Removal level. default:%(default)s",
                        default=3)
    args = parser.parse_args()

    def remove_header(elem, doc):
        if type(elem) == pf.Header:
            if elem.level > args.level:
                return []

    return pf.run_filter(remove_header)


if __name__ == "__main__":
    sys.exit(main())
