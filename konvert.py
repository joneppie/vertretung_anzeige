#!/usr/bin/python3

import Konverter

###Einzelseiten
config = Konverter.ConfigLeser('einzelseiten',  False)
if config.isExist():
    pfade = config.getPflichtWert('pfade')
    zweitage = config.getPflichtWert('zweitage')
    template = config.getWert('template', 'Templates/plan.tmpl')
    aktTag = config.getWert('aktTag', '')
    nextTag = config.getWert('nextTag',  '')
    ausgabe = config.getWert('ausgabe',  '_out')

    einzelseiten = Konverter.Einzelseiten(template, zweitage,  aktTag,  nextTag,  ausgabe)
    for pfad in pfade.split():
        einzelseiten.konvert(pfad)

###Mehfrachseite
config = Konverter.ConfigLeser('mehrfachseite',  False)
if config.isExist():
    pfade = config.getPflichtWert('pfade')
    template = config.getWert('template', 'Templates/plan.tmpl')
    #mehrfachseite = Konverter.Mehrfachseite(template)
    #for pfad in pfade.split():
      #  mehrfachseite.konvert(pfad)
