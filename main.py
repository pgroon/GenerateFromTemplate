from lxml import etree as ET
from zipfile import ZipFile
import os
import argparse


parser = argparse.ArgumentParser(description='Generate greeting letter from template and user data./n'
                                             'Required data: NAME, EMAIL, PASSWORD, COMPUTER, ROOM,/n '
                                             'USERNAME, PRINTER, TEMPLATE-FILENAME')
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
    if not (element.text is None) and (marker in element.text):
        key = element.text.split("__")[0]
        element.text = data.get(key)

# 4. Generate new XML file
filename = "./content1.xml"
with open(filename, 'wb') as destFile:
    tree.write(destFile, xml_declaration=True, pretty_print=True, encoding='utf-8')

# 5. Generate zip file and rename to .odt
dirName = r'/home/grunwald/exp/test'
outFileName = 'welcome_' + data['LAST']
os.chdir(os.path.dirname(dirName))
with zipfile.ZipFile((outFileName + '.odt'),
                     "w",
                     zipfile.ZIP_DEFLATED,
                     allowZip64=True) as zf:
    for root, _, filenames in os.walk(os.path.basename(dirName)):
        for name in filenames:
            name = os.path.join(root, name)
            name = os.path.normpath(name)
            zf.write(name, name)


#TODO:   6. Move new file to proper location (Wherever that is)

#print(ET.tostring(tree, encoding="unicode", pretty_print=True))
#print('-------------')
