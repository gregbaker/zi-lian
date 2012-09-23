#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, sys
from zelian import create_worksheet
#import cgitb
#cgitb.enable()

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
            'guidewidth': 0.3,
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
    print "Content-type: application/pdf"
    print 'Content-disposition: inline; filename="worksheet.pdf"'
    print
    create_worksheet(sys.stdout)


main()
