from lxml import html
from lxml import etree
import os
import re
import Konverter
import shutil
import glob
import time

class Einzelseiten:
    def __init__(self, template,  zweitage,  aktTag,  nextTag,  ausgabe,  platzhalter):
        self.template = template
        self.zweitage = zweitage
        self.aktTag = aktTag
        self.nextTag = nextTag
        self.ausgabe = ausgabe
        self.zeiten = None
        self.platzhalter = platzhalter

    def konvert(self,  pfad):
        if self.zweitage == '1':
            self.zeiten = Konverter.Zeiten(pfad + self.aktTag + self.ausgabe)
            if self.zeiten.readTime() < Konverter.Zeiten.getToday():
                self.moveToNewDay(pfad)
            else:
                self._konvertTeile(pfad + self.aktTag)
                self._konvertTeile(pfad + self.nextTag)
        else:
            self.zeiten = Konverter.Zeiten(pfad + self.ausgabe)
            self.zeiten.readTime()
            self._konvertTeile(pfad)

    def _konvertTeile(self, pfad):
        files = os.listdir(pfad + '/')
        files = sorted(files)

        for file in files:
            if not re.match('subst_', file): #nur Units-Dateien
                continue
            if os.path.getmtime(pfad + '/' + file) < self.zeiten.getTime(): #nur neuere Dateien
                continue
            #Templatedatei neu laden
            tmplTree = html.parse(self.template)
            tmplBody = tmplTree.find('body')
            tmplRefresh = tmplTree.xpath("//meta[@http-equiv='refresh']")[0]

            tree = html.parse(pfad + '/' + file)
            kopfkaesten = tree.xpath("//table[@class='info']")
            titles = tree.xpath("//div[@class='mon_title']")
            listen = tree.xpath("//table[@class='mon_list']")
            refresh = tree.xpath("//meta[@http-equiv='refresh']")
            refreshdata = refresh[0].attrib['content'] #Daten zu den Refreshzeiten holen
            refreshtime = refreshdata.split(';')[0]
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

            tmplBody.insert(1, center)
            tmplBody.insert(2, listen[0])

            tmplRefresh.attrib['content'] = refreshdata
            tmplBody.attrib['onload'] = "countdown(" + refreshtime + ",5)"

            tmplTree.write(pfad + self.ausgabe + '/' + file, pretty_print=True)
            self.zeiten.writeTime()

    def moveToNewDay(self,  path):
        for file in glob.glob(path + self.nextTag + self.ausgabe + "/subst_*"):
            shutil.copy(file,  path + self.aktTag + self.ausgabe)
        shutil.copy(self.platzhalter,  path + self.nextTag + self.ausgabe + "/subst_001.htm")
        self.zeiten.writeTime()

    def konvertSperre(self,  pfad,  sperrzeitBeginn,  sperrzeitEnde,  sperrzeitAnzeige):
        if self.zweitage == '1': #Zeiten auslesen
            self.zeiten = Konverter.Zeiten(pfad + self.aktTag + self.ausgabe)
        else:
            self.zeiten = Konverter.Zeiten(pfad + self.ausgabe)
        self.zeiten.readTime()
        if ( # In der Sperrzeit?
                self.zeiten.getTime() < Konverter.Zeiten.getTimeToday(sperrzeitBeginn)
                and Konverter.Zeiten.getTimeToday(sperrzeitBeginn) < time.time()
                and time.time() < Konverter.Zeiten.getTimeToday(sperrzeitEnde)
            ):
            if self.zweitage == '1':
                shutil.copy(pfad + self.nextTag + self.ausgabe + "/subst_001.htm",  pfad + self.nextTag + self.ausgabe + "/subst_sicherung_001.htm")
                shutil.copy(sperrzeitAnzeige,  pfad + self.nextTag + self.ausgabe + "/subst_001.htm")
                shutil.copy(pfad + self.aktTag + self.ausgabe + "/subst_001.htm",  pfad + self.aktTag + self.ausgabe + "/subst_sicherung_001.htm")
                shutil.copy(sperrzeitAnzeige,  pfad + self.aktTag + self.ausgabe + "/subst_001.htm")
            else:
                shutil.copy(pfad + self.ausgabe + "/subst_001.htm",  pfad + self.ausgabe + "/subst_sicherung_001.htm")
                shutil.copy(sperrzeitAnzeige,  pfad + self.ausgabe + "/subst_001.htm")
            self.zeiten.writeTime()
        elif ( # Nach der Sperrzeit?
                Konverter.Zeiten.getTimeToday(sperrzeitBeginn) < self.zeiten.getTime()
                and self.zeiten.getTime() < Konverter.Zeiten.getTimeToday(sperrzeitEnde)
                and Konverter.Zeiten.getTimeToday(sperrzeitEnde) < time.time()
            ):
            if self.zweitage == '1':
                shutil.copy(pfad + self.nextTag + self.ausgabe + "/subst_sicherung_001.htm",  pfad + self.nextTag + self.ausgabe + "/subst_001.htm")
                shutil.copy(pfad + self.aktTag + self.ausgabe + "/subst_sicherung_001.htm",  pfad + self.aktTag + self.ausgabe + "/subst_001.htm")
            else:
                shutil.copy(pfad + self.ausgabe + "/subst_sicherung_001.htm",  pfad + self.ausgabe + "/subst_001.htm")
            self.zeiten.setTimeToBeginn()
            self.konvert(pfad)
        else:
            self.konvert(pfad)


if __name__ == "__main__":
    print("Klasse ist nicht direkt aufrufbar")
