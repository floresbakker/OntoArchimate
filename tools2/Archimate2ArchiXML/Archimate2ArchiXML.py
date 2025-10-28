# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:40:53 2023

@author: Flores Bakker

The XML2RDF script offers a simple way of transforming an XML-document into a representation of the XML-code in RDF-based triples. Just set your base directory and place there your own XML-document so that the script can transform this to RDF-format.

"""

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from rdflib import Graph, Namespace, Literal, RDF
import os

from rdflib.namespace import NamespaceManager

# Get the current working directory in which the file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir, '..'))

# namespace declaration
rdf         = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs        = Namespace("http://www.w3.org/2000/01/rdf-schema#")
doc         = Namespace("https://data.rijksfinancien.nl/archixml/doc/id/")
archiXML    = Namespace("https://data.rijksfinancien.nl/archixml/model/def/")
xml         = Namespace("http://www.w3.org/XML/model/def/")
xmlns       = Namespace("http://www.w3.org/2000/xmlns/model/def/")
xlink       = Namespace("https://www.w3.org/1999/xlink/model/def/")
xsi         = Namespace("http://www.w3.org/2001/XMLSchema-instance/model/def/")

# function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding = 'utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

def generate_node_id(node):
    # Base case: If there's no parent, return an empty string (root-level element)
    if node.parent is None:
        return "1"

    # Initialize the sibling index for the current element
    sibling_index = 1
    # Count previous siblings (including text and non-element nodes)
    for sibling in node.previous_siblings:
        sibling_index += 1

    # Recursive call: Get the parent's ID
    parent_id = generate_node_id(node.parent)

    # If the parent ID is not empty, append the current element's sibling index
    if parent_id:
        return f"{parent_id}.{sibling_index}"
    else:
        return str(sibling_index)  # This happens at the root level

# loop through any xml files in the input directory
for filename in os.listdir(directory_path+"/OntoArchimate/Tools/Archimate2ArchiXML/Input"):
    if filename.endswith(".xml"):
        file_path = os.path.join(directory_path+"/OntoArchimate/Tools/Archimate2ArchiXML/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # place the xml code in a string
        xml_doc = readGraphFromFile (file_path)

        # initialize graph
        g = Graph(bind_namespaces="rdflib")      
      
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)
        g.bind("archiXML", archiXML)
        g.bind("xml", xml)
        g.bind("xmlns", xmlns)
        g.bind("xlink", xlink)
        g.bind("xsi", xsi)

        # fill graph with archiXML vocabulary
        xml_graph = Graph().parse(directory_path+"/OntoArchimate/Specification/archiXML - core.ttl" , format="ttl")

        # string for query to establish IRI of a 'tag' XML node
        tagquerystring = '''
            
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix xml: <http://www.w3.org/XML/model/def/>

        select ?node_IRI where {
          ?node_IRI xml:tag ?tag
        }
        '''

        # parse xml document
        soup = BeautifulSoup(xml_doc, features="xml")
        root_node = soup.contents[0]
        root_id = generate_node_id(root_node)

        # loop through each node in the XML document
        for node in soup.descendants:
            # check if the node is an XML tag node
            if isinstance(node, Tag):
                # establish unique id for the XML tag node
                node_id = generate_node_id(node)
                
                # establish IRI for the tag class based on the XML vocabulary
                tag_result = xml_graph.query(tagquerystring, initBindings={"tag" : Literal(node.name)})
                for row in tag_result:
                    tag_IRI = row.node_IRI
                    
                # add the node to the graph with its unique identifier as IRI and its tag as type
                g.add((doc[node_id], RDF.type, tag_IRI))
                
                # add a document node as a container of the XML-tree
                if node.name == 'model':
                    document_id = '1'
                    g.add((doc[document_id], RDF.type, archiXML["Document"]))
                    g.add((doc[document_id], rdf["_" + str(document_id)], doc[node_id]))
        
                # establish optional attributes of the node
                for attribute, values in node.attrs.items():
                    # Check if it's the default namespace declaration
                    if attribute == 'xmlns':
                        namespace_uri = xml
                        local_name = 'xmlns'
                    # Split attribute name into namespace and local name
                    elif ':' in attribute:
                        namespace, local_name = attribute.split(':')
                        # Check the namespace of the attribute and add appropriate RDF triple
                        if namespace == 'xml':
                            namespace_uri = xml
                        elif namespace == 'xlink':
                            namespace_uri = xlink
                        elif namespace == 'xsi':
                            namespace_uri = xsi
                        elif namespace == 'xmlns':
                            namespace_uri = xmlns
                        elif namespace == 'archiXML':
                            namespace_uri = archiXML
                        else:
                            namespace_uri = None  # Unknown namespace prefix
                    else:
                        namespace_uri = archiXML
                        local_name = attribute 
        
                    # If namespace is found, add RDF triple
                    if namespace_uri:
                        # If the attribute consists of multiple values (as list), join them
                        if isinstance(values, list):
                            attribute_value = ' '.join(values)
                        else:  # If it's a single value, keep it as is
                            attribute_value = values
                        # Add optional attributes of the node to the graph
                        g.add((doc[node_id], namespace_uri[local_name], Literal(attribute_value)))
                    
                # go through the direct children of the node
                member_count = 0 # initialize count
                for child in node.children:
                    member_count = member_count + 1 # count the number of direct children, so that we can establish the sequence of appearance of the children within the parent node, through the 'rdf:_x' property between parent and child.
                    
                    # if the child is an xml tag node get its unique identifier based on sourceline and sourcepos
                    if isinstance(child, Tag):
                      if child.name == None  :
                          childname = ""
                      else:
                          childname = child.name
                      child_id = generate_node_id(child)
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))
                      
                    # if the child is an text node, create a unique identifier based on sourceline and sourcepos of its parent and the sequence position of the child within the parent, as the xml-parser does not have sourceline and sourcepos available as attributes for text nodes.
                    elif isinstance(child, NavigableString):
                      if child.name == None  :
                            childname = "Text"
                      else:
                            childname = child.name
                      child_id = generate_node_id(child)
                      
                      # write to graph that the parent node has a child with a certain sequence position
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child node is of type Text
                      g.add((doc[child_id], RDF.type, archiXML["Text"]))
                      
                      # empty content (of type None) in xml needs to be converted to empty string
                      if node.string == None: 
                          text_fragment = "" 
                      else:
                          text_fragment = node.string
                      
                      # write string content of the text node to the graph
                      g.add((doc[child_id], xml["fragment"], Literal(text_fragment)))

        # write the resulting graph to file
        g.serialize(destination=directory_path+"/OntoArchimate/Tools/Archimate2ArchiXML/Output/" + filename_stem + "-parsed.ttl", format="turtle")
        
        print ("\nArchimate file '", filename,"' is succesfullly transformed to file", filename_stem + "-parsed.ttl in Turtle format.")
    else: 
        print ('\nWarning: file in directory "input" is no archimate file and cannot be parsed.')
