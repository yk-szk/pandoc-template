import sys
import os
from pathlib import Path
import argparse
from docxcompose.composer import Composer
from docx import Document as Document_compose
from logzero import logger

def main():
    if os.name != 'nt':
        print('Windows only script!')
        return 1

    parser = argparse.ArgumentParser(description='Convert docx to pdf.')
    parser.add_argument('input', help='Input docx filename. default: %(default)s',metavar='<filename>', nargs='?', default='dissertation.docx')
    parser.add_argument('-o', '--output', help='Output pdf filename.',metavar='<filename>', type=str)
    # parser.add_argument('-s','--switch', help='Switch argument',action='store_true')

    args = parser.parse_args()
    import win32com.client
    wdFormatPDF = 17
    word = win32com.client.DispatchEx("Word.Application")
    doc = word.Documents.Open(str(Path(args.input).resolve()))

    if False:
        logger.info('Update ToC')
        word.ActiveDocument.TablesOfContents(1).Update()

    if args.output is None:
        args.output = Path(args.input).with_suffix('.pdf')

    args.output = Path(args.output).with_suffix('.pdf').resolve()
    if str(args.output)=='.':  # saving in the cwd and the pdf file does not exist 
        args.output = Path('.').resolve() / args.pdf
    logger.info('Save as pdf %s', args.output)
    doc.SaveAs(str(Path(args.output).resolve()), FileFormat=wdFormatPDF)

    doc.Close(SaveChanges=True)

    word.Quit()


    logger.info('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())