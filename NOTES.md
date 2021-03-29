Notes
=====

Handling images
---------------

Convert extensions to lowecase:
```
for x in `fd .JPG`; do echo "${x%.*}.jpg"; done
```
Resize to 1024px wide:
```
for x in `fd .jpg`; do echo $x; sips -Z 1024 $x; done
```
