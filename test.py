from xml.dom.minidom import parseString

xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
    <entry key="com.bigdata.rdf.sail.truthMaintenance">false</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.textIndex">false</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.justify">false</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers">false</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.axiomsClass">com.bigdata.rdf.axioms.NoAxioms</entry>
    <entry key="com.bigdata.rdf.sail.namespace">lala</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.quads">false</entry>
    <entry key="com.bigdata.rdf.store.AbstractTripleStore.geoSpatial">false</entry>
    <entry key="com.bigdata.journal.Journal.groupCommit">false</entry>
    <entry key="com.bigdata.namespace.lala.spo.com.bigdata.btree.BTree.branchingFactor">1024</entry>
    <entry key="com.bigdata.rdf.sail.isolatableIndices">false</entry>
    <entry key="com.bigdata.namespace.lala.lex.com.bigdata.btree.BTree.branchingFactor">400</entry>
</properties>
"""

root = parseString(xml)
elements = root.getElementsByTagName('entry')
hehe = {}
for child in elements:
    key = child.attributes.get('key').nodeValue
    value = child.firstChild.nodeValue
    hehe[key] = value

textHehe = ''

for key, value in hehe.items():
    textHehe += f"{key}={value}\n"

print(textHehe)