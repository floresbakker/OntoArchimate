# Specification 'Archimate Ontology'

This is the repository for the Archimate Ontology, an RDF-based vocabulary for representing Archimate terms and logic. You're welcome to contribute!

The Archimate Ontology provides a comprehensive description of the Archimate vocabulary, encompassing the elements and relationships that constitute Archimate documents. Additionally, it includes algorithms for generating, parsing, validating, annotating, and reusing Archimate documents.

# Status

Unstable, work in progress. Still trying to understand the subtleties of the Archimate language. From reading blogs it seems that the Archimate language itself still has interoperability issues, meaning that in different applications a architectural design will be shown differently or with errors.

# Background

In the field of enterprise architecture, Archimate plays a crucial role in modeling and analyzing complex systems and architectures. Archimate provides a standardized framework for describing the structure, behavior, and relationships within organizations, facilitating communication and decision-making processes.

However, the representation of Archimate models in traditional formats lacks the semantic richness necessary for interoperability and advanced analysis. The Archimate Ontology addresses this limitation by formalizing Archimate concepts and relationships in RDF format, leveraging semantic web technologies to enhance interoperability, integration, and semantic understanding of Archimate models.

With the Archimate Ontology, users can generate, parse, validate, annotate, and reuse Archimate documents using semantic web compliant technology, unlocking new possibilities for leveraging Archimate models within the wider context of the Semantic Web.

# Introduction

Let us explore the semantic Archimate vocabulary with examples of Archimate models.

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
@prefix xml1: <http://www.w3.org/XML/model/def/> .
@prefix xmlns: <http://www.w3.org/2000/xmlns/model/def/> .
@prefix xsi: <http://www.w3.org/2001/XMLSchema-instance/model/def/> .

model:BasicModel-Document a archiXML:Document ;
    rdf:_1 model:BasicModel-Model .

model:BasicModel-Model a archiXML:Model ;
    rdf:_1 model:BasicModel-ModelName ;
    rdf:_2 model:BasicModel-Documentation ;
    rdf:_3 model:BasicModel-Elements ;
    rdf:_4 model:BasicModel-Relationships ;
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
    xml1:fragment "Example of a basic model with two elements and a relationship" .

model:BasicModel-Elements a archiXML:Elements ;
    rdf:_1 model:aApplicationComponent-Element ;
    rdf:_2 model:aBusinessActor-Element ;
    rdf:_3 model:aBusinessObject-Element ;
    rdf:_4 model:aBusinessRole-Element .
    
model:BasicModel-Relationships a archiXML:Relationships ;
    rdf:_1 model:aRelationship1-Relationship ;
    rdf:_2 model:aRelationship2-Relationship .

model:aApplicationComponent-Element a archiXML:Element ;
    rdf:_1 model:aApplicationComponent-ElementName ;
    xsi:type "ApplicationComponent" ;
    prov:wasDerivedFrom model:aApplicationComponent ;
    archiXML:identifier "ApplicationComponent1" .

model:aApplicationComponent-ElementName a archiXML:Name ;
    rdf:_1 model:aApplicationComponent-ElementNameText ;
    xml1:lang "en" .

model:aApplicationComponent-ElementNameText a archiXML:Text ;
    xml1:fragment "An application component" .

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
    xml1:fragment "A business role" .

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
```

The above mentioned archiXML code can then be serialized using the ArchiXML - core vocabulary together with the XML core vocabulary, the latter containing the serialisation algorithm to produce actual XML:

```
<model xmlns="http://www.opengroup.org/xsd/archimate/3.0/" identifier="Model-1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.1/archimate3_Model.xsd">
    <name xml:lang="en">Basic Model</name>
    <documentation xml:lang="en">Example of a basic model with two elements and a relationship</documentation>
    <elements>
        <element identifier="ApplicationComponent1" xsi:type="ApplicationComponent">
            <name xml:lang="en">An application component</name>
        </element>
        <element identifier="BusinessActor1" xsi:type="BusinessActor">
            <name xml:lang="en">A business actor</name>
        </element>
        <element identifier="BusinessObject1" xsi:type="BusinessObject">
            <name xml:lang="en">A business role</name>
        </element>
        <element identifier="BusinessRole1" xsi:type="BusinessRole">
            <name xml:lang="en">A business role</name>
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
</model>
```

We can also roundtrip from the XML back to the RDF-based archiXML back to the RDF-based archimate core vocabulary. This means that one can parse archimate documents made in tools like Archi and then convert them to RDF, provided one uses the open exchange XML-based format for Archimate.


# Tools and dependencies

This repository comes with three, fairly primitive, Python-based tools to handle Archimate-documents and RDF-representations of Archimate. 

1. ArchiVoc2ArchiXML
2. ArchiXML2Archimate
3. Archimate2ArchiXML

## Archimate2RDF

The tool Archimate2RDF is used to read Archimate-documents, parse them and then transform them to RDF-based triples. 

### How to use Archimate2RDF

A. Install all necessary libraries:

	1. pip install os 
	2. pip install bs4
	3. pip install rdflib

B. Place one or more Archimate-files in the input folder in OntoArchimate\Tools\Archimate2RDF\Input. Only ordinary Archimate-files can be processed. 

C. Run the script in the command prompt by typing: 

```
python Archimate2RDF.py
```

D. Go to the output folder in OntoArchimate\Tools\Archimate2RDF\Output and grab your Turtle-file(s) (*.ttl). 


## RDF2Archimate

The tool RDF2Archimate is used to read a RDF-based representation of an Archimate-document into a graph and then serialize and save this to an actual Archimate-file. 

### How to use RDF2Archimate

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

NOTE: pyshacl has a dependency with an older RDFlib version. However, for an optimal functioning of the semantic Archimate-vocabulary, the most recent release of RDFlib should be used. Hence, it is advised to first install pyshacl and then RDFlib, so that RDFlib is installed having the latest version. This is currently the least instrusive way of handling the dependency, offering accessibility for those not well versed in Python. 

B. Place one or more Turtle-files (*.ttl) in the input folder in OntoArchimate\Tools\RDF2Archimate\Input. A Turtle-file should represent a Archimate-document using the Archimate-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python RDF2Archimate.py
```

D. Go to the output folder in OntoArchimate\Tools\RDF2Archimate\Output and grab your Archimate-file(s). Additionally included are Turtle-file(s) (*.ttl) that contain the serialized 'archimate:fragment' properties for the very same Archimate-document and the Archimate-elements it contains. 


## Dependencies 

Both tools make extensive use of [RDFlib](https://rdflib.readthedocs.io/en/stable/index.html). Rdflib is a Python library used for working with Resource Description Framework (RDF) data. RDF is a widely used framework for representing and processing information on the web. It is a standard model for data interchange on the web, particularly for representing metadata and data about resources available on the internet.

Rdflib provides a comprehensive set of tools and utilities for working with RDF data, including parsing and serializing RDF in various formats (such as RDF/XML, Turtle, JSON-LD, and more), querying RDF data using SPARQL, creating RDF graphs, and performing various operations on RDF triples.

The RDF2Archimate tool additionally makes use of [PyShacl](https://github.com/RDFLib/pySHACL). PySHACL is a complete open-source implementation of the SHACL W3C specification, with broad use in the community as well. 

# Acknowledgements

We would like to thank Iwan Aucamp @RDFlib for his unrelenting support and accomplishments regarding the open source triple store and related services, as well as Ashley Sommer @PyShacl for his work on the important open source implementation of a SHACL engine. 