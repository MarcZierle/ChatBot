FILE?=doc

.PHONY: pdf %.pdf
.FORCE:

%.pdf: $(FILE).tex .FORCE 
	xelatex $(FILE).tex

pdf: $(FILE).pdf
	gio open $(FILE).pdf
