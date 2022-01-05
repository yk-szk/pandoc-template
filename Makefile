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

UNAME = $(shell uname)
ifeq ($(UNAME),Darwin) # macOS
	INKSCAPE = /Applications/Inkscape.app/Contents/MacOS/inkscape
else
	INKSCAPE = /mnt/c/Program\ Files/Inkscape/bin/inkscape.com
	ifneq (,$(wildcard $(INKSCAPE))) # linux
		INKSCAPE = inkscape
		# (native) inkscape does not work in WSL without below
		export _INKSCAPE_GC=disable
	endif
endif

output/%.pdf: %.tex
	latexmk -pdf -g -pdflatex="pdflatex -interaction=nonstopmode" -output-directory=output $<

PANDOC_OPTS = -s --metadata-file metadata.yaml -F pandoc-crossref
%.tex: %.md $(PDF_IMAGES) templates/template.tex
	pandoc $(PANDOC_OPTS) -F script/imgconv.py -F script/remove_header.py --biblatex --template templates/template.tex $< -t latex | grep -v -e \\tightlist -e \\labelenumi > $@

%.html: %.md $(SVG_IMAGES) templates/styles.css metadata.yaml
	pandoc $(PANDOC_OPTS) --katex -c templates/styles.css --template templates/template.html --citeproc --toc --toc-depth=4 --section-divs -H templates/nav_script.html $< -o $@

%.docx: %.md $(EMF_IMAGES)
	pandoc $(PANDOC_OPTS) -F script/imgconv.py -F script/remove_header.py --citeproc --reference-doc=templates/style.docx $< -o $@

image/%.emf: image/original/%.svg
	$(INKSCAPE) $< --export-filename=$@

# pdf files are converted in imgconv.py
$(PDF_IMAGES): $(SVG_IMAGES)

image/%.svg: image/original/%.svg
	$(INKSCAPE) $< -l --export-filename=$@

# docx -> pdf
WINPYTHON = /mnt/c/Users/${USER}/Anaconda3/python.exe
%.pdf: %.docx
	$(WINPYTHON) script/docx2pdf.py $<