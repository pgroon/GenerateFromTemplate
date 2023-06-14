from lxml import etree as ET
import zipfile as ZF
import tempfile as TF
import os
import shutil
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
homeDir = r'/home/user/template-dir/'
outFileName = 'welcome_' + data['LAST']
marker = "__"
data['NAME'] = (data['FIRST'] + ' ' + data['LAST'])
template = os.path.join(homeDir, data['TEMPLATE'])

# 1. Open and parse dara from the template's "content.xml"
archive = ZF.ZipFile(template, 'r')
tmplXML = archive.open('content.xml')
tree = ET.parse(tmplXML)

# 3. Perfom search/replace on the tree
for element in tree.iter():
    if not (element.text is None) and (marker in element.text):
        key = element.text.split("__")[0]
        element.text = data.get(key)

# 4. Generate new XML file
xmlNewFile = os.path.join(homeDir, "contentNew.xml")
with open(xmlNewFile, 'wb') as destFile:
    tree.write(destFile, xml_declaration=True, pretty_print=True, encoding='utf-8')

# create temporary folder
tmpDir = TF.TemporaryDirectory()

# unzip template.odt contents into the temp folder
archive.extractall(tmpDir.name)

# delete the original "content.xml" from the temp folder
os.chdir(tmpDir.name)
if os.path.exists("content.xml"):
    os.remove("content.xml")
else:
    print("Failed to locate the template's content.xml")

# add the newly generated xml file to temp folder
os.rename(xmlNewFile, os.path.join(tmpDir.name, "content.xml"))

# zip the temp folder *contents* to new archive
shutil.make_archive(os.path.join(homeDir, outFileName), 'zip', tmpDir.name)

# delete temp folder
tmpDir.cleanup()

# rename .zip to .odt and move to final location
os.rename(os.path.join(homeDir, (outFileName + '.zip')) , os.path.join(homeDir, (outFileName + '.odt')))

# FOR DIAGNOSTICS:
#print(ET.tostring(tree, encoding="unicode", pretty_print=True))
