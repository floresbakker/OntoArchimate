# Specification 'Archimate Ontology'

This is the repository for the Archimate Ontology, an RDF-based vocabulary for representing Archimate terms and logic. You're welcome to contribute!

The Archimate Ontology provides a comprehensive description of the Archimate vocabulary, encompassing the elements and relationships that constitute Archimate documents. Additionally, it includes algorithms for generating, parsing, validating, annotating, and reusing Archimate documents.

# Status

Unstable, work in progress.

# Background

In the field of enterprise architecture, Archimate plays a crucial role in modeling and analyzing complex systems and architectures. Archimate provides a standardized framework for describing the structure, behavior, and relationships within organizations, facilitating communication and decision-making processes.

However, the representation of Archimate models in traditional formats lacks the semantic richness necessary for interoperability and advanced analysis. The Archimate Ontology addresses this limitation by formalizing Archimate concepts and relationships in RDF format, leveraging semantic web technologies to enhance interoperability, integration, and semantic understanding of Archimate models.

With the Archimate Ontology, users can generate, parse, validate, annotate, and reuse Archimate documents using semantic web compliant technology, unlocking new possibilities for leveraging Archimate models within the wider context of the Semantic Web.

# Introduction

Let us explore the semantic Archimate vocabulary with examples of Archimate models.

## Example #1: An Archimate model representing a 'Purchasing' application

```<?xml version="1.0" encoding="UTF-8"?>
<archimate:model xmlns="http://www.archimatetool.com/archimate" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="OntoArchimate" id="id-377d65038f614b3885cbdf30304d02ae" version="5.0.0">
  <folder name="Application" id="id-3d6f2fbf1f0743e6904d70cd318eb080" type="application">
    <element xsi:type="archimate:ApplicationComponent" name="Purchasing" id="id-2dab151425234cebaec68c56edfcdf2b"/>
  </folder>
 /folder>
  <folder name="Views" id="id-7e0e0ced065441d1a96e56e667b51fbb" type="diagrams">
    <element xsi:type="archimate:ArchimateDiagramModel" name="Default View" id="id-7f2d44f14c5f468892a4d46ccc0dde09">
      <child xsi:type="archimate:DiagramObject" id="id-6254d9d15058420a8dd73b711dadb2e6" archimateElement="id-2dab151425234cebaec68c56edfcdf2b">
        <bounds x="487" y="251" width="120" height="55"/>
      </child>
    </element>
  </folder>
</archimate:model>
```
This graphic is rendered in a browser as follows:

![An example of an Archimate-document](/Examples/ArchimateExample.JPG)

## Expressing the Archimate-document in RDF

Now we can represent the very same document in <i>RDF</i> using the Archimate-vocabulary. As it is very cumbersome to do so by hand, a <i>Archimate2RDF</i> tool is available in this repository that will do exactly that for you. For further information on this tool and other neat tools, scroll down this Readme file.

```
@prefix archimate: <https://data.rijksfinancien.nl/archimate/model/def/> .
@prefix doc: <https://data.rijksfinancien.nl/archimate/doc/id/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml1: <http://www.w3.org/XML/1998/namespace#> .
@prefix xmlns: <http://www.w3.org/2000/xmlns/> .
@prefix xsi: <http://www.w3.org/2001/XMLSchema-instance#> .

doc:1 a archimate:Document ;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/0/0> .

<https://data.rijksfinancien.nl/archimate/doc/id/0/0> a archimate:Model ;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/00/1> ;
    rdf:_2 <https://data.rijksfinancien.nl/archimate/doc/id/00/3> ;
    xmlns:archimate "http://www.archimatetool.com/archimate" ;
    xmlns:xsi "http://www.w3.org/2001/XMLSchema-instance" ;
    xml1:xmlns "http://www.archimatetool.com/archimate" ;
    archimate:id "id-377d65038f614b3885cbdf30304d02ae" ;
    archimate:name "OntoArchimate" ;
    archimate:version "5.0.0" .

<https://data.rijksfinancien.nl/archimate/doc/id/00/1> a archimate:Folder ;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/100/1> ;
    archimate:id "id-3d6f2fbf1f0743e6904d70cd318eb080" ;
    archimate:name "Application" ;
    archimate:type "application" .

<https://data.rijksfinancien.nl/archimate/doc/id/100/1> a archimate:Element ;
    xsi:type "archimate:ApplicationComponent" ;
    archimate:id "id-2dab151425234cebaec68c56edfcdf2b" ;
    archimate:name "Purchasing" .

<https://data.rijksfinancien.nl/archimate/doc/id/00/3> a archimate:Folder ;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/300/1> ;
    archimate:id "id-7e0e0ced065441d1a96e56e667b51fbb" ;
    archimate:name "Views" ;
    archimate:type "diagrams" .

<https://data.rijksfinancien.nl/archimate/doc/id/300/1> a archimate:Element ;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/1300/1> ;
    xsi:type "archimate:ArchimateDiagramModel" ;
    archimate:id "id-7f2d44f14c5f468892a4d46ccc0dde09" ;
    archimate:name "Default View" .

<https://data.rijksfinancien.nl/archimate/doc/id/1300/1> a archimate:Child ;;
    rdf:_1 <https://data.rijksfinancien.nl/archimate/doc/id/11300/1> ;
    xsi:type "archimate:DiagramObject" ;
    archimate:archimateElement "id-2dab151425234cebaec68c56edfcdf2b" ;
    archimate:id "id-6254d9d15058420a8dd73b711dadb2e6" .

<https://data.rijksfinancien.nl/archimate/doc/id/11300/1> a archimate:Bounds ;
    archimate:height "55" ;
    archimate:width "120" ;
    archimate:x "487" ;
    archimate:y "251" .

```

Make note on how each element in the Archimate-document is identified by a unique identifier, the IRI (Internationalized Resource Identifier). Now we can address each element, or combinations of elements, and say something about them. Either we express meaning (RDF, RDFS, OWL and more), or impose constraints (SHACL) or we can query (SPARQL) them to know more about them.


# Tools and dependencies

This repository comes with two, fairly primitive, Python-based tools to handle Archimate-documents and RDF-representations of Archimate. 

1. Archimate2RDF 
2. RDF2Archimate



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