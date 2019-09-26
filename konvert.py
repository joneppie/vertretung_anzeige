#!/usr/bin/python3

import Konverter

config = Konverter.ConfigLeser('mehrfachseite')
pfade = config.getPflichtWert('pfade')
template = config.getWert('template', 'Templates/plan.tmpl')

mehrfachseite = Konverter.Mehrfachseite(template)
for pfad in pfade.split():
    mehrfachseite.konvert(pfad + '/')
