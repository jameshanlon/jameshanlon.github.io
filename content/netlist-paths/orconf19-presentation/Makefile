NAME = slides

all: $(NAME).pdf

$(NAME).pdf: $(NAME).tex
	pdflatex $(NAME).tex

clean:
	rm -f *.aux *.log *.err *.out
	rm -f *.toc *.blg *.bbl *.lof
