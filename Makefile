.PHONY: all clean gitclean

all: manuscript.docx manuscript.html manuscript.pdf

clean:
	latexmk -CA

gitclean:
	git clean -fx

%.pdf: %.tex
	latexmk -pdf -g -pdflatex="pdflatex -interaction=nonstopmode" $<

%.tex: %.md
	pandoc -s --metadata-file metadata.yaml -F pandoc-crossref -F script/imgconv.py -F script/remove_header.py --biblatex --template templates/template.tex $< -t latex | grep -v -e \\tightlist -e \\labelenumi > $@

%.html: %.md templates/styles.css metadata.yaml
	pandoc -s --katex -c templates/styles.css --template templates/template.html --metadata-file metadata.yaml -F pandoc-crossref --citeproc --toc --toc-depth=4 --section-divs -H templates/nav_script.html $< -o $@

%.docx: %.md
	pandoc -s --metadata-file metadata.yaml -F script/imgconv.py -F script/remove_header.py -F pandoc-crossref --citeproc $< -o $@
