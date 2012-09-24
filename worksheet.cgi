#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, sys
#import cgitb
#cgitb.enable()

try:
    from local_config import *
except ImportError:
    pass

from zilian import create_worksheet
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import CMYKColor

def main():
    # collect CGI input from form
    form = cgi.FieldStorage()
    try:
        size = float(form.getvalue('size'))
    except (TypeError, ValueError):
        size = 17
    guidestyle = form.getvalue('guidestyle') or '*'
    nameline = 'nameline' in form

    # create style dict for worksheet
    style = {
            'pagewidth': 8.5*inch,
            'pageheight': 11*inch,
            'sqwidth': size*mm,
            'sqheight': size*mm,
            'outlinecolor': CMYKColor(0,0,0,1),
            'outlinewidth': 0.5,
            'guidestyle': guidestyle,
            'guidecolor': CMYKColor(0,0,0,0.2),
            'guidewidth': 0.5,
            'guidedash': [2, 2],
            'topmargin': 0.75*inch,
            'leftmargin': 0.75*inch,
            'linesep': size/10*mm,
            'sqsep': 0*inch,
            'nameline': nameline,
            'namefontsize': 12,
            }
    style['bottommargin'] = style['topmargin']
    
    if style['nameline']:
        style['topmargin'] += style['namefontsize'] + style['linesep']
    
    style['squares'] = int((style['pagewidth'] - 2*style['leftmargin']) / (style['sqwidth'] + style['sqsep']))
    style['lines'] = int((style['pageheight'] - style['topmargin'] - style['bottommargin']) / (style['sqheight'] + style['linesep']))
    
    # build the sheet and return
    out = sys.stdout
    out.write("Content-type: application/pdf\n")
    out.write('Content-disposition: inline; filename="worksheetx.pdf"\n\n')
    create_worksheet(out, style)


main()
