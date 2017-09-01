#!/usr/bin/python3

from string import Template
import sys
import csv
import os

if len(sys.argv) != 3:
    print("Usage:\n", sys.argv[0], "CONFIG.conf ZIELPFAD\n")
    sys.exit(0)

seiten = []
links = ""
i = 0
with open(sys.argv[1], newline='') as csvfile:
        seitenDatei = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in seitenDatei:
                seiten.append(row)
                links = links + '<a style="margin-left:50px;" href="seite_' + str(i) + '.html">' + row[1] + '</a>\n'
                i = i + 1

eigenerPfad = os.path.dirname(os.path.realpath(__file__))

vorlage = open(eigenerPfad + '/Templates/SelectPage.tmpl', 'r')
vorl_inhalt = vorlage.read()
vorlage.close()

i = 0
for seite in seiten:
    template = Template(vorl_inhalt)
    ersetzungen = { 'Link' : seite[0], 'Title' : row[1], 'Links' : links }
    neueSeite = template.substitute(ersetzungen)
    outfile = open(sys.argv[2] + '/seite_' + str(i) + '.html', 'w')
    outfile.write(neueSeite)
    outfile.close()
    i = i + 1