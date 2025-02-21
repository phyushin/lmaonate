from PyPDF2 import PdfWriter as Writer, PdfReader as Reader
from PyPDF2.generic import AnnotationBuilder
import argparse

__maj__ = 1
__min__ = 0
__rev__ = 3

__author__ = "Phyu"


__version__ = f"{__maj__}.{__min__}.{__rev__}"
page_box = [
        0,
        0,
        612,
        792
    ]

output = Writer()

def banner():
    if not args.quiet:
        print(f"""
              
░  ░░░░░░░░  ░░░░  ░░░      ░░░░      ░░░░░░░░░   ░░░  ░░░      ░░░        ░░        ░
▒  ▒▒▒▒▒▒▒▒   ▒▒   ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒▒    ▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒▒▒
▓  ▓▓▓▓▓▓▓▓        ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓  ▓  ▓▓  ▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓      ▓▓▓
█  ████████  █  █  ██        ██  ████  ████████  ██    ██        █████  █████  ███████
█        ██  ████  ██  ████  ███      █████████  ███   ██  ████  █████  █████        █
                                                                                     
                                                                               
Version: {__version__}
Author: {__author__}
              """)



parser = argparse.ArgumentParser(
    prog='lmaonate',
    description='A python script to add whole page links into PDFs rather than have to pay for acrobat writer'
)

parser.add_argument("-i","--infile",dest="infile", required=True)
parser.add_argument("-o","--outfile",dest="outfile", required=True)
parser.add_argument("-u","--url",dest="url", required=True)
parser.add_argument("-q",dest="quiet", action="store_true")

args = parser.parse_args() 



def modify_pdf(infile_path: str, outfile_path: str):
    url = args.url
    print(f"Adding link '{url}' to PDF saved to '{outfile_path}'")
    
    with open (infile_path, "rb") as f:
        pdf = Reader(f)
        meta = pdf.metadata

        output.add_metadata({
            "/Title": f"{meta.title}",
            "/Producer":f"{meta.producer}"
            }
        )

        page_count = len(pdf.pages)
        
        for i in range(page_count):
            p = pdf.pages[i]
            output.add_page(p)
           
            link = AnnotationBuilder.link(page_box, None, url=url)          
            output.add_annotation(page_number=i,annotation= link)
            
            with open(outfile_path,"wb") as out_stream:
                output.write(out_stream)

def main():
    banner()
    modify_pdf(args.infile, args.outfile)

if __name__ == "__main__":
    main()