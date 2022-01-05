.PHONY: all clean gitclean

all: manuscript.docx manuscript.html output/manuscript.pdf

clean:
	latexmk -CA

gitclean:
	git clean -fx

ORIGINAL_IMAGES = $(wildcard image/original/*.svg)
SVG_IMAGES = $(subst original/,,$(ORIGINAL_IMAGES))
EMF_IMAGES = $(SVG_IMAGES:.svg=.emf)
PDF_IMAGES = $(SVG_IMAGES:.svg=.pdf)
INKSCAPE = /mnt/c/Program\ Files/Inkscape/bin/inkscape.com

output/%.pdf: %.tex
	latexmk -pdf -g -pdflatex="pdflatex -interaction=nonstopmode" -output-directory=output $<

%.tex: %.md $(PDF_IMAGES) templates/template.tex
	pandoc -s --metadata-file metadata.yaml -F pandoc-crossref -F script/imgconv.py -F script/remove_header.py --biblatex --template templates/template.tex $< -t latex | grep -v -e \\tightlist -e \\labelenumi > $@

%.html: %.md $(SVG_IMAGES) templates/styles.css metadata.yaml
	pandoc -s --katex -c templates/styles.css --template templates/template.html --metadata-file metadata.yaml -F pandoc-crossref --citeproc --toc --toc-depth=4 --section-divs -H templates/nav_script.html $< -o $@

%.docx: %.md $(EMF_IMAGES)
	pandoc -s --metadata-file metadata.yaml -F script/imgconv.py -F script/remove_header.py -F pandoc-crossref --citeproc --reference-doc=templates/style.docx $< -o $@


# (native) inkscape does not work in WSL without below
# export _INKSCAPE_GC=disable

image/%.emf: image/original/%.svg
	$(INKSCAPE) $< --export-filename=$@

$(PDF_IMAGES): $(SVG_IMAGES)
# pdf files are converted in imgconv.py

image/%.svg: image/original/%.svg
	$(INKSCAPE) $< -l --export-filename=$@


# docx -> pdf
winpython = /mnt/c/Users/${USER}/Anaconda3/python.exe
%.pdf: %.docx
	$(winpython) script/docx2pdf.py $<