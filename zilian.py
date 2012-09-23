#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import inch, mm

def draw_square(c, x, y, style):
    """
    Draw a single character square with specified style.
    """
    w = style['sqwidth']
    h = style['sqheight']

    # draw guides first so they are under the outline strokes
    c.setStrokeColor(style['guidecolor'])
    c.setLineWidth(style['guidewidth'])
    c.setDash(style['guidedash'])
    
    if style['guidestyle'] in ['+', '*']:
        c.line(x+w/2, y, x+w/2, y+h)
        c.line(x, y+h/2, x+w, y+h/2)
    if style['guidestyle'] in ['X', '*']:
        c.line(x, y, x+w, y+h)
        c.line(x, y+h, x+w, y)
    if style['guidestyle'] == '#':
        c.line(x, y+h/3, x+w, y+h/3)
        c.line(x, y+2*h/3, x+w, y+2*h/3)
        c.line(x+w/3, y, x+w/3, y+h)
        c.line(x+2*w/3, y, x+2*w/3, y+h)

    # outline
    c.setStrokeColor(style['outlinecolor'])
    c.setLineWidth(style['outlinewidth'])
    c.setFillColor(CMYKColor(black=0, alpha=0))
    c.setDash()

    c.rect(x, y, w, h, fill=0)


def draw_line(c, y, style):
    """
    Draw a line of character squares with the specified style.
    """
    w = style['sqwidth']
    sep = style['sqsep']
    for i in range(style['squares']):
        draw_square(c, style['leftmargin'] + w*i + sep*i, y, style)


def draw_sheet(c, style):
    """
    Draw a worksheet with the specified style, on the given canvas.
    """
    if style['nameline']:
        c.setFont('Helvetica', style['namefontsize'])
        c.drawString(style['leftmargin'],
                style['pageheight'] - style['topmargin'] + style['linesep'],
                'Name:')
        c.drawString(style['leftmargin'] + style['pagewidth']/2,
                style['pageheight'] - style['topmargin'] + style['linesep'], 
                'Date:')

    y = style['pageheight'] - style['topmargin'] - style['sqheight']
    for i in range(style['lines']):
        draw_line(c, y, style)
        y -= style['sqheight'] + style['linesep']


def create_worksheet(stream, style):
    """
    Output a PDF worksheet to the given stream (or filename).
    """
    c = canvas.Canvas(stream, pagesize=(style['pagewidth'], style['pageheight']))
    draw_sheet(c, style)
    c.showPage()
    c.save()
            
