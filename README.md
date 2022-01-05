# My pandoc template
Write once in markdown and produce documents in multiple formats (docx, pdf, html).

Example [markdown](manuscript.md)

## Setup
- [pandoc](https://pandoc.org/installing.html)
- [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)
- (Optional) [inkscape](https://inkscape.org) 

WSL environment is recommended for .docx to .pdf conversion.

## Commands
```sh
make # make html, docx and pdf
make manuscript.html
make manuscript.docx
make output/manuscript.pdf
```

## Usage
- Store SVG images in `image/original`
- Create .bib file
  - Use reference manager such as [zotero](https://www.zotero.org) with Better BibTeX.
- [utility scripts](script/README.md)
