from xml.etree import ElementTree
import os

DEFAULT_SOURCE = """
while true do
    local p = Instance.New("Part")
    p.Size = Vector3.New(3,3,3)
    p.Color3 = Color3.Random()
    p.Position = script.Parent.Position
    p.Anchored = false
    wait(0.1)
    end
"""


def add_script(parent, scriptName='Script', source=None):
    script = ElementTree.SubElement(parent, "Item")
    script.attrib = {'class': 'Script'}

    properties = ElementTree.SubElement(script, "Properties")

    name = ElementTree.SubElement(properties, "string")
    name.attrib = {"name": "name"}
    name.text = scriptName

    source = ElementTree.SubElement(properties, "string")
    source.attrib = {"name": "source"}
    source.text = source and source or DEFAULT_SOURCE


tree = ElementTree.parse('parse.spm')
game = tree.getroot()

environment = None
scriptService = None

for child in list(game):
    attributes = child.attrib
    if attributes["class"] == "Environment":
        environment = child
    elif attributes["class"] == "ScriptService":
        scriptService = child

Parts = []

for part in list(environment):
    attributes = part.attrib
    if 'class' in attributes:
        Parts.append(part)

for filename in os.listdir('build'):
    if filename.endswith('.lua'):
        with open(os.path.join('build', filename)) as f:
            content = f.read()

            path = filename.split("#")

            scriptName = path[len(path) - 1][:-4]

            path.pop(len(path) - 1)

            currentElement = scriptService

            if len(path) > 0:
                for part in Parts:
                    Properties = list(part)[0]

                    if Properties.tag != "Properties":
                        continue

                    PartName = list(Properties)[0].text

                    if PartName == path[0]:
                        currentElement = part

            add_script(currentElement, scriptName, content)

tree.write('out/result.spm')
