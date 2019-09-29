from lxml import html
from lxml import etree
import os
import re

class Einzelseiten:
    def __init__(self, template,  zweitage,  aktTag,  nextTag,  ausgabe):
        self.template = template
        self.zweitage = zweitage
        self.aktTag = aktTag
        self.nextTag = nextTag
        self.ausgabe = ausgabe

    def konvert(self,  pfad):
        if self.zweitage == '1':
            self._konvertTeile(pfad + self.aktTag)
            self._konvertTeile(pfad + self.nextTag)
        else:
            self._konvertTeile(pfad)

    def _konvertTeile(self, pfad):
        files = os.listdir(pfad + '/')
        files = sorted(files)

        for file in files:
            if not re.match('subst_', file): #nur Units-Dateien
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

if __name__ == "__main__":
    print("Klasse ist nicht direkt aufrufbar")