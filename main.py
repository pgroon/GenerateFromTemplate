from lxml import etree as ET
from zipfile import ZipFile
import tempfile, os, argparse


parser = argparse.ArgumentParser(description='Generate greeting letter from template and user data./n'
                                             'Required data: NAME, EMAIL, PASSWORD, COMPUTER, ROOM, USERNAME, PRINTER, TEMPLATE-FILENAME')
parser.add_argument("FIRST", help="Vorname", type=str)
parser.add_argument("LAST", help="Nachname", type=str)
parser.add_argument("EMAIL", help="Email addresse", type=str)
parser.add_argument("PWD", help="Erstpasswort", type=str)
parser.add_argument("COMP", help="Zugewiesener Computer", type=str)
parser.add_argument("ROOM", help="Raumnummer", type=str)
parser.add_argument("HANDLE", help="Benutzername", type=str)
parser.add_argument("PRINT", help="Zugewiesener Drucker", type=str)
parser.add_argument("TEMPLATE", help="name der Template-Datei inkl. der Dateiendung", type=str)

# Turn CLI-arguments into a modifiable dictionary:
data = vars(parser.parse_args())

# Define some more variables:
marker = "__"
data['NAME'] = (data['FIRST'] + ' ' + data['LAST'])
template = os.path.join(r'/home/grunwald/exp/', data['TEMPLATE'])

# 1. Open and parse dara from the template's "content.xml"
archive = ZipFile(template, 'r')
tmplXML = archive.open('content.xml')
tree = ET.parse(tmplXML)

# 3. Perfom search/replace on the tree
for element in tree.iter():
    if not (element.text == None) and (marker in element.text):
        key = element.text.split("__")[0]
        element.text = data.get(key)

# 4. Generate new XML file
filename = "./content1.xml"
with open(filename, 'wb') as destFile:
    tree.write(destFile, xml_declaration=True, pretty_print=True, encoding='utf-8')

#TODO:   5. Export final file
#TODO:       5.1 Extract .odt
#TODO:       5.2 replace old content.xml with the newly generated one
#TODO:       5.3 zip the contents again and convert to .odt
#TODO:       5.4 export as PDF (?)
#TODO:   6. Move new file to proper location (Wherever that is)

#print(ET.tostring(tree, encoding="unicode", pretty_print=True))
#print('-------------')
