.PHONY: all clean
all: main.pdf

main.pdf: main.tex references.bib
	latexmk -pdf -interaction=nonstopmode main.tex

clean:
	latexmk -C
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.synctex.gz *.toc

distclean: clean
	rm -f main.pdf
