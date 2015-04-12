PNG_FILES = $(patsubst %.ly,%.png,$(wildcard *.ly))

all: $(PNG_FILES)

clean:
	rm -f *.pdf *.tex *.texi *.count *.eps

%.pdf: %.ly
	lilypond $<

%.png: %.pdf
	sips -s format png $< --out $@
