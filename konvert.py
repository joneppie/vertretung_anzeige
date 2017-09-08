#!/usr/bin/python3

from lxml import html
from lxml import etree
import os
import Konverter
import re

config = Konverter.ConfigLeser('mehrfachseite')
pfad = config.getPflichtWert('pfad') + '/'
template = config.getWert('template', 'Templates/plan.tmpl')

tmplTree = html.parse(template)
tmplBody = tmplTree.find('body')

files = os.listdir(pfad)
files = sorted(files)

i = 0
for file in files:
    if not re.match('subst_', file): #nur Units-Dateien
        continue
    tree = html.parse(pfad + file)
    kopfkaesten = tree.xpath("//table[@class='info']")
    titles = tree.xpath("//div[@class='mon_title']")
    listen = tree.xpath("//table[@class='mon_list']")
    absaetze = tree.xpath("//td/p")
    for text in absaetze[0].itertext():
        if text.find("Stand")>0:
            stand = text
    standspan = etree.SubElement(titles[0], "span")
    standspan.text = stand
    standspan.attrib['style'] = "font-size: 60%; font-weight: normal"

    center = etree.Element("center")
    center.insert(0, titles[0])
    if len(kopfkaesten) > 0:
        center.insert(1, kopfkaesten[0])

    tmplBody.insert(i, center)
    tmplBody.insert(i+1, listen[0])

    i = i+2

tmplTree.write(pfad + 'plan.html', pretty_print=True)
