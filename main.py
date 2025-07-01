#!/usr/bin/env python3

from PyPDF2 import PdfWriter as Writer, PdfReader as Reader
from PyPDF2.generic import AnnotationBuilder
import argparse

__maj__ = 1
__min__ = 0
__rev__ = 7

__author__ = "Phyu"


__version__ = f"{__maj__}.{__min__}.{__rev__}"

""" ANSI color codes """
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
ENDC = "\033[0m"

a4_page_box = [
        0,
        0,
        612,
        792
    ]

ERROR= 0
WARN= 1
INF=2
OUT=3
DBG=4

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
dbg = False
parser.add_argument("-i","--infile",dest="infile", required=True)
parser.add_argument("-o","--outfile",dest="outfile", required=True)
parser.add_argument("-u","--url",dest="url", required=True)
parser.add_argument("-q",dest="quiet", action="store_true")
parser.add_argument("-d","--debug", dest="debug", action="store_true")
args = parser.parse_args() 

dbg=args.debug

def fancy_print(level: int, message: str):
    bullet = "[*]"
    if level == ERROR:
        bullet = f"[{RED}!{ENDC}]"
    elif level == WARN:
        bullet = f"[{YELLOW}!{ENDC}]"
    elif level == INF:
        bullet = f"[{BLUE}*{ENDC}]"
    elif level == OUT:
        bullet = f"[{GREEN}*{ENDC}]"
    elif level == DBG:
        if dbg:
            bullet = f"[{BLUE}?{ENDC}]"
    else:
        bullet = "[*]" #it should already be this but we need to initialise it
    print (f"{bullet} - {message}")

def err_print(message: str):
    fancy_print(ERROR, message)

def warn_print(message: str):
    fancy_print(WARN, message)

def inf_print(message: str):
    fancy_print(INF, message)

def out_print(message: str):
    fancy_print(OUT, message)

def dbg_print(message: str):
    fancy_print(DBG, message)

def modify_pdf(infile_path: str, outfile_path: str):
    url = args.url
    out_print(f"Adding link '{url}' to PDF saved to '{outfile_path}'")
    
    with open (infile_path, "rb") as f:
        pdf = Reader(f)
        meta = pdf.metadata

        dbg_print(meta)

        output.add_metadata({
            "/Author":f"{meta.author}",
            "/Creator":f"{meta.creator}",
            "/CreationDate":f"{meta.creation_date_raw}",
            "/ModDate":f"{meta.modification_date_raw}",
            "/Title": f"{meta.title}",
            "/Producer":f"{meta.producer}"
            }
        )

        page_count = len(pdf.pages)
        
        for i in range(page_count):
            p = pdf.pages[i]
            output.add_page(p)
           
            link = AnnotationBuilder.link(a4_page_box, None, url=url)          
            output.add_annotation(page_number=i, annotation=link)
            
            with open(outfile_path,"wb") as out_stream:
                output.write(out_stream)

def main():
    banner()
    modify_pdf(args.infile, args.outfile)

if __name__ == "__main__":
    main()
