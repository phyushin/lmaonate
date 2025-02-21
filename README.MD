# LMAONATE

---

Pronounced Laminate

### What Is It?

Lmaonate is a python script to inject hyperlinks over the pages of a PDF document ... for phishing purposes (with prior permission obviously)

### Why?

Because I didn't want to have to buy Adobe acrobat :eyes:

### How To Use
Generate your legitimate pdf, then call lmaonate with the pdf as the input (`-i`) and whatever name you would like the output (`-o`) file to have, specifying the link to insert.
there's also a `-q` flag to hide the banner


#### Example
`./main.py -i <legit_doc.pdf> -o <output_doc.pdf> -u <url for the link>`