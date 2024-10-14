# Specification 'OntoArchimate'

This is the repository for the OntoArchimate ontology, a family of RDF-based vocabularies to represent Archimate terms and logic. You're welcome to contribute!

The OntoArchimate familiy of ontologies provides a comprehensive description of the Archimate vocabulary, encompassing the elements and relationships that constitute Archimate documents. Additionally, it includes algorithms for generating, parsing, validating, annotating, and reusing Archimate documents.

The family of OntoArchimate consists of the following four vocabularies:

1. Archimate Core Vocabulary
2. Archimate Serialisation Vocabulary
3. ArchiXML Core Vocabulary
4. ArchiXML Serialisation Vocabulary

With OntoArchimate one can describe architecture according to the Archimate standard, using the RDF-based Archimate Core Vocabulary. From here, we can transform this architecture to a RDF-based model of an XML document representing that architecture, using the ArchiXML Core Vocabulary and ArchiXML Serialisation Vocabulary. Finally, we can serialize this to an actual XML document using the XML Core Vocabulary. We can also roundtrip this process and start with an XML file, parse it to the ArchiXML vocabulary then serialize it to the Archimate Core Vocabulary, using the Archimate Serialisation Vocabulary.

![Overview OntoArchimate Objects](/Examples/OntoArchimateObjects.JPG)

OntoArchimate also makes use of another family of vocabularies:

1. DOM Core Vocabulary
2. XML Core Vocabulary
3. XMLNS Core Vocabulary
4. XLINK Core Vocabulary
5. XSI Core Vocabulary

These five vocabularies are used for generating, parsing, validating, annotating, and reusing XML-based documents.

# Status

Unstable, work in progress. 

# Background

In the field of enterprise architecture, Archimate plays a crucial role in modeling and analyzing complex systems and architectures. Archimate provides a standardized framework for describing the structure, behavior, and relationships within organizations, facilitating communication and decision-making processes.

However, the representation of Archimate models in traditional formats lacks the semantic richness necessary for interoperability and advanced analysis. The Archimate Ontology addresses this limitation by formalizing Archimate concepts and relationships in RDF format, leveraging semantic web technologies to enhance interoperability, integration, and semantic understanding of Archimate models.

With the Archimate Ontology, users can generate, parse, validate, annotate, and reuse Archimate documents using semantic web compliant technology, unlocking new possibilities for leveraging Archimate models within the wider context of the Semantic Web.

# Introduction

Let us explore the OntoArchimate family of vocabularies with examples of Archimate models.

## Example #1: Basic Archimate model with three elements and two relationships:

In this example we consider an Archimate model consisting of three Archimate elements...

1. a Business Actor
2. a Business Role
3. a Business Object

...and two relationships:

1. An Assignment Relationship from the Business Actor to the Business Role, representing the assignment of a role to the actor. 
2. An Association Relationship from the Business Object to the Assignment Relationship. 

Relationship 2 is thus connecting a Business Object with relationship 1.

![Example #1](/Examples/ArchimateExample1.JPG)

This can be represented in RDF using the archimate vocabulary as follows:

```
prefix archimate: <https://data.rijksfinancien.nl/archimate/model/def/>
prefix model: <https://data.rijksfinancien.nl/archimate/id/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>

### Model

model:BasicModel 
    rdf:type archimate:Model;
    skos:prefLabel "Basic Model";
    skos:definition "Example of a basic model with three elements and two relationships".

### Element

model:aBusinessActor 
    rdf:type archimate:BusinessActor;
    skos:prefLabel "A business actor";
    skos:definition "An example of a business actor";
    rdfs:isDefinedBy model:BasicModel.

model:aBusinessRole 
    rdf:type archimate:BusinessRole;
    skos:prefLabel "A business role";
    skos:definition "An example of a business role";
    rdfs:isDefinedBy model:BasicModel.
    
model:aBusinessObject
    rdf:type archimate:BusinessObject;
    skos:prefLabel "A business role";
    skos:definition "An example of a business role";
    rdfs:isDefinedBy model:BasicModel.
   
### Relationship

model:aRelationship1 
    rdf:type archimate:Relationship;
    skos:prefLabel "a business actor - role assignment";
    skos:definition "An example of a business actor and role assignment";
    archimate:from model:aBusinessActor;
    archimate:relationship archimate:assignedTo;
    archimate:to model:aBusinessRole;
    rdfs:isDefinedBy model:BasicModel.  
   
model:aRelationship2
    rdf:type archimate:Relationship;
    skos:prefLabel "a business object - relationship association";
    skos:definition "An example of a business object and relationship association";
    archimate:from model:aBusinessObject;
    archimate:relationship archimate:association;
    archimate:to model:aRelationship1;
    rdfs:isDefinedBy model:BasicModel.  
```

In turn this archimate model can be generated to a RDF-representation of an XML-document describing the archimate model, using the Archimate - Serialisation vocabulary and archiXML vocabulary, both of which are also offered by this repository. The result of processing the RDF-based archimate model into an RDF-based archiXML vocabulary model, looks like this:

```
@prefix archiXML: <https://data.rijksfinancien.nl/archixml/model/def/> .
@prefix archimate: <https://data.rijksfinancien.nl/archimate/model/def/> .
@prefix model: <https://data.rijksfinancien.nl/archimate/id/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml1: <http://www.w3.org/XML/model/def/> .
@prefix xmlns: <http://www.w3.org/2000/xmlns/model/def/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix xsi: <http://www.w3.org/2001/XMLSchema-instance/model/def/> .

# Model

model:BasicModel-Document a archiXML:Document ;
    rdf:_1 model:BasicModel-Model .

model:BasicModel-Model a archiXML:Model ;
    rdf:_1 model:BasicModel-ModelName ;
    rdf:_2 model:BasicModel-Documentation ;
    rdf:_3 model:BasicModel-Elements ;
    rdf:_4 model:BasicModel-Relationships ;
    rdf:_5 model:BasicModel-Views ;
    xmlns:xsi "http://www.w3.org/2001/XMLSchema-instance" ;
    xsi:schemaLocation "http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.1/archimate3_Model.xsd" ;
    xml1:xmlns "http://www.opengroup.org/xsd/archimate/3.0/" ;
    prov:wasDerivedFrom model:BasicModel ;
    archiXML:identifier "Model-1" .

model:BasicModel-ModelName a archiXML:Name ;
    rdf:_1 model:BasicModel-ModelNameText ;
    xml1:lang "en" .

model:BasicModel-ModelNameText a archiXML:Text ;
    xml1:fragment "Basic Model" .
    
model:BasicModel-Documentation a archiXML:Documentation ;
    rdf:_1 model:BasicModel-DocumentationText ;
    xml1:lang "en" .

model:BasicModel-DocumentationText a archiXML:Text ;
    xml1:fragment "Example of a basic model with two elements and two relationships" .

# Elements

model:BasicModel-Elements a archiXML:Elements ;
    rdf:_1 model:aBusinessActor-Element ;
    rdf:_2 model:aBusinessObject-Element ;
    rdf:_3 model:aBusinessRole-Element .

model:aBusinessActor-Element a archiXML:Element ;
    rdf:_1 model:aBusinessActor-ElementName ;
    xsi:type "BusinessActor" ;
    prov:wasDerivedFrom model:aBusinessActor ;
    archiXML:identifier "BusinessActor1" .

model:aBusinessActor-ElementName a archiXML:Name ;
    rdf:_1 model:aBusinessActor-ElementNameText ;
    xml1:lang "en" .

model:aBusinessActor-ElementNameText a archiXML:Text ;
    xml1:fragment "A business actor" .

model:aBusinessObject-Element a archiXML:Element ;
    rdf:_1 model:aBusinessObject-ElementName ;
    xsi:type "BusinessObject" ;
    prov:wasDerivedFrom model:aBusinessObject ;
    archiXML:identifier "BusinessObject1" .

model:aBusinessObject-ElementName a archiXML:Name ;
    rdf:_1 model:aBusinessObject-ElementNameText ;
    xml1:lang "en" .

model:aBusinessObject-ElementNameText a archiXML:Text ;
    xml1:fragment "A business object" .

model:aBusinessRole-Element a archiXML:Element ;
    rdf:_1 model:aBusinessRole-ElementName ;
    xsi:type "BusinessRole" ;
    prov:wasDerivedFrom model:aBusinessRole ;
    archiXML:identifier "BusinessRole1" .

model:aBusinessRole-ElementName a archiXML:Name ;
    rdf:_1 model:aBusinessRole-ElementNameText ;
    xml1:lang "en" .

model:aBusinessRole-ElementNameText a archiXML:Text ;
    xml1:fragment "A business role" .

# Relationships

model:BasicModel-Relationships a archiXML:Relationships ;
    rdf:_1 model:aRelationship1-Relationship ;
    rdf:_2 model:aRelationship2-Relationship .

model:aRelationship1-Relationship a archiXML:Relationship ;
    rdf:_1 model:aRelationship1-RelationshipName ;
    xsi:type "Assignment" ;
    prov:wasDerivedFrom model:aRelationship1 ;
    archiXML:identifier "Relation_1" ;
    archiXML:source "BusinessActor1" ;
    archiXML:target "BusinessRole1" .

model:aRelationship1-RelationshipName a archiXML:Name ;
    rdf:_1 model:aRelationship1-RelationshipNameText ;
    xml1:lang "en" .

model:aRelationship1-RelationshipNameText a archiXML:Text ;
    xml1:fragment "Assignment Relationship"@en .

model:aRelationship2-Relationship a archiXML:Relationship ;
    rdf:_1 model:aRelationship2-RelationshipName ;
    xsi:type "Association" ;
    prov:wasDerivedFrom model:aRelationship2 ;
    archiXML:identifier "Relation_2" ;
    archiXML:source "BusinessObject1" ;
    archiXML:target "Relation_1" .

model:aRelationship2-RelationshipName a archiXML:Name ;
    rdf:_1 model:aRelationship2-RelationshipNameText ;
    xml1:lang "en" .

model:aRelationship2-RelationshipNameText a archiXML:Text ;
    xml1:fragment "Association Relationship"@en .

# Views

model:BasicModel-Views a archiXML:Views ;
    rdf:_1 model:BasicModel-Views-Diagrams .

model:BasicModel-Views-Diagrams a archiXML:Diagrams ;
    rdf:_1 model:aView-View .
    
model:aView a archimate:View ;
    rdf:_1 model:aBusinessActor ;
    rdf:_2 model:aBusinessRole ;
    rdf:_3 model:aBusinessObject ;
    rdf:_4 model:aRelationship1 ;
    rdf:_5 model:aRelationship2 ;
    rdfs:isDefinedBy model:BasicModel ;
    skos:definition "An example of an archimate view" ;
    skos:prefLabel "A view" .

model:aView-View a archiXML:View ;
    rdf:_1 model:aView-ViewName ;
    rdf:_2 model:aView-Viewnode_BusinessActor1 ;
    rdf:_3 model:aView-Viewnode_BusinessRole1 ;
    rdf:_4 model:aView-Viewnode_BusinessObject1 ;
    rdf:_5 model:aView-Viewconnection_Relation_1 ;
    rdf:_6 model:aView-Viewconnection_Relation_2 ;
    xsi:type "Diagram" ;
    prov:wasDerivedFrom model:aView ;
    archiXML:identifier "View_1" .

model:aView-ViewName a archiXML:Name ;
    rdf:_1 model:aView-ViewNameText ;
    xml1:lang "en" .

model:aView-ViewNameText a archiXML:Text ;
    xml1:fragment "A view" .

model:aView-Viewnode_BusinessActor1 a archiXML:Node ;
    xsi:type "Element" ;
    archiXML:elementRef "BusinessActor1" ;
    archiXML:h 55 ;
    archiXML:identifier "node_BusinessActor1" ;
    archiXML:w 120 ;
    archiXML:x 300 ;
    archiXML:y 0 .

model:aView-Viewnode_BusinessObject1 a archiXML:Node ;
    xsi:type "Element" ;
    archiXML:elementRef "BusinessObject1" ;
    archiXML:h 55 ;
    archiXML:identifier "node_BusinessObject1" ;
    archiXML:w 120 ;
    archiXML:x 600 ;
    archiXML:y 0 .

model:aView-Viewnode_BusinessRole1 a archiXML:Node ;
    xsi:type "Element" ;
    archiXML:elementRef "BusinessRole1" ;
    archiXML:h 55 ;
    archiXML:identifier "node_BusinessRole1" ;
    archiXML:w 120 ;
    archiXML:x 450 ;
    archiXML:y 0 .
    
model:aView-Viewconnection_Relation_1 a archiXML:Connection ;
    xsi:type "Relationship" ;
    archiXML:identifier "connection_Relation_1" ;
    archiXML:relationshipRef "Relation_1" ;
    archiXML:source "node_BusinessActor1" ;
    archiXML:target "node_BusinessRole1" .

model:aView-Viewconnection_Relation_2 a archiXML:Connection ;
    xsi:type "Relationship" ;
    archiXML:identifier "connection_Relation_2" ;
    archiXML:relationshipRef "Relation_2" ;
    archiXML:source "node_BusinessObject1" ;
    archiXML:target "connection_Relation_1" .
```

The above mentioned archiXML code can then be serialized using the ArchiXML - core vocabulary together with the XML core vocabulary, the latter containing the serialisation algorithm to produce an actual XML document:

```
<model xmlns="http://www.opengroup.org/xsd/archimate/3.0/" identifier="Model-1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.1/archimate3_Model.xsd">
    <name xml:lang="en">Basic Model</name>
    <documentation xml:lang="en">Example of a basic model with two elements and two relationships</documentation>
    <elements>
        <element identifier="BusinessActor1" xsi:type="BusinessActor">
            <name xml:lang="en">A business actor</name>
        </element>
        <element identifier="BusinessObject1" xsi:type="BusinessObject">
            <name xml:lang="en">A business object</name></element>
        <element identifier="BusinessRole1" xsi:type="BusinessRole"><
            name xml:lang="en">A business role</name>
        </element>
    </elements>
    <relationships>
        <relationship identifier="Relation_1" source="BusinessActor1" target="BusinessRole1" xsi:type="Assignment">
            <name xml:lang="en">Assignment Relationship</name>
        </relationship>
        <relationship identifier="Relation_2" source="BusinessObject1" target="Relation_1" xsi:type="Association">
            <name xml:lang="en">Association Relationship</name>
        </relationship>
    </relationships>
    <views>
        <diagrams>
            <view identifier="View_1" xsi:type="Diagram">
                <name xml:lang="en">A view</name>
                <node identifier="node_BusinessActor1" elementRef="BusinessActor1" h="55" w="120" y="0" x="300" xsi:type="Element"></node>
                <node identifier="node_BusinessRole1" elementRef="BusinessRole1" h="55" w="120" y="0" x="450" xsi:type="Element"></node>
                <node identifier="node_BusinessObject1" elementRef="BusinessObject1" h="55" w="120" y="0" x="600" xsi:type="Element"></node>
                <connection identifier="connection_Relation_1" relationshipRef="Relation_1" source="node_BusinessActor1" target="node_BusinessRole1" xsi:type="Relationship"></connection>
                <connection identifier="connection_Relation_2" relationshipRef="Relation_2" source="node_BusinessObject1" target="connection_Relation_1" xsi:type="Relationship"></connection>
            </view>
        </diagrams>
    </views>
</model>
```

This XML document can be read into Archimate based tooling and visualised as follows:

![Example #1](/Examples/ArchimateExample1.JPG)

We can also roundtrip from the XML document back to the RDF-based archiXML back to the RDF-based archimate core vocabulary. This means that one can parse archimate documents made in tools like Archi, BizzDesign and the like, and then convert them to RDF, provided one uses the open exchange XML-based format for Archimate.


# Tools and dependencies

This repository comes with three, fairly primitive, Python-based tools to handle Archimate-documents and RDF-representations of Archimate. 

1. ArchiVoc2ArchiXML
2. ArchiXML2Archimate
3. Archimate2ArchiXML
4. ArchiXML2ArchiVoc


## ArchiVoc2ArchiXML

The tool ArchiVoc2ArchiXML is used to read an RDF-based representation of an Archimate model into a graph and then serialize and save this to an RDF-based representation of the XML-based archimate document that contains this model, using the ArchiXML vocabulary.

### How to use ArchiVoc2ArchiXML

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

B. Place one or more Turtle-files (*.ttl) in the input folder in OntoArchimate\Tools\ArchiVoc2ArchiXML\Input. A Turtle-file should represent an RDF-based Archimate-document using the Archimate-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python ArchiVoc2ArchiXML.py
```

D. Go to the output folder in OntoArchimate\Tools\ArchiVoc2ArchiXML\Output and grab your turtle-file(s). 


## ArchiXML2Archimate

The tool ArchiXML2Archimate is used to read a RDF-based representation of an XML-based Archimate document into a graph and then serialize and save this to an actual XML-based Archimate-file. 

### How to use ArchiXML2Archimate

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

B. Place one or more Turtle-files (*.ttl) in the input folder in OntoArchimate\Tools\ArchiXML2Archimate\Input. A Turtle-file should represent an XML-based  Archimate-document using the ArchiXML-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python ArchiXML2Archimate.py
```

D. Go to the output folder in OntoArchimate\Tools\ArchiXML2Archimate\Output and grab your Archimate-file(s). Additionally included are Turtle-file(s) (*.ttl) that contain the serialized 'xml:fragment' properties for the very same Archimate-document and the Archimate elements, relationships and views it contains. 


## Archimate2ArchiXML

The tool Archimate2ArchiXML is used to read Archimate-documents, parse them and then transform them to RDF-based triples. 

### How to use Archimate2ArchiXML

A. Install all necessary libraries:

	1. pip install os 
	2. pip install bs4
	3. pip install rdflib

B. Place one or more Archimate-files in the input folder in OntoArchimate\Tools\Archimate2ArchiXML\Input. Only ordinary Archimate-files based on the open exchange XML format can be processed. 

C. Run the script in the command prompt by typing: 

```
python Archimate2ArchiXML.py
```

D. Go to the output folder in OntoArchimate\Tools\Archimate2ArchiXML\Output and grab your Turtle-file(s) (*.ttl). 


## ArchiXML2ArchiVoc

The tool ArchiXML2ArchiVoc is used to read an RDF-based ArchiXML representation of an Archimate XML file into a graph and then serialize and save this to an RDF-based archimate model, using the Archimate Core vocabulary.

### How to use ArchiXML2ArchiVoc

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

B. Place one or more Turtle-files (*.ttl) in the input folder in OntoArchimate\Tools\ArchiXML2ArchiVoc\Input. A Turtle-file should represent an RDF-based ArchiXML model using the ArchiXML-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python ArchiXML2ArchiVoc.py
```

D. Go to the output folder in OntoArchimate\Tools\ArchiXML2ArchiVoc\Output and grab your turtle-file(s). 


## Dependencies 

All tools make extensive use of [RDFlib](https://rdflib.readthedocs.io/en/stable/index.html). Rdflib is a Python library used for working with Resource Description Framework (RDF) data. RDF is a widely used framework for representing and processing information on the web. It is a standard model for data interchange on the web, particularly for representing metadata and data about resources available on the internet.

Rdflib provides a comprehensive set of tools and utilities for working with RDF data, including parsing and serializing RDF in various formats (such as RDF/XML, Turtle, JSON-LD, and more), querying RDF data using SPARQL, creating RDF graphs, and performing various operations on RDF triples.

Two out of three tools additionally makes use of [PyShacl](https://github.com/RDFLib/pySHACL). PySHACL is a complete open-source implementation of the SHACL W3C specification, with broad use in the community as well. 

# Acknowledgements

We would like to thank Iwan Aucamp @RDFlib for his unrelenting support and accomplishments regarding the open source triple store and related services, as well as Ashley Sommer @PyShacl for his work on the important open source implementation of a SHACL engine. 