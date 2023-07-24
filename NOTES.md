Notes
=====

Handling images
---------------

Convert HEIC to JPG:
```
brew install imagemagick
mogrify -format jpg *.HEIC
```

Convert extensions to lowecase:
```
for x in `fd .JPG`; do echo "${x%.*}.jpg"; done
```

Resize to 1024px wide:
```
for x in `fd .jpg`; do echo $x; sips -Z 1024 $x; done
```

Convert SVG or PDF to PNG:
```
convert -verbose -resize 1000x -density 150 -trim -quality 100 -flatten <infile.{svg,pdf}> <out.png>
```
