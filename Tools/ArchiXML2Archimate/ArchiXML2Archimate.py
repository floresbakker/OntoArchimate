# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:42:53 2023

@author: Flores Bakker

"""
import pyshacl
import rdflib 
import os

# Get the current working directory in which the file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir, '..'))

# Function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

# Function to write a graph to a file
def writeGraph(graph):
    graph.serialize(destination=directory_path+"/OntoArchimate/Tools/ArchiXML2Archimate/Output/"+filename_stem+"-serialized.ttl", format="turtle")

# Function to call the PyShacl engine so that a RDF model of a Archimate document can be serialized to Archimate-code.
def iteratePyShacl(vocabulary, serializable_graph):
        
        # call PyShacl engine and apply the Archimate vocabulary to the serializable Archimate document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=vocabulary,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
        
        # Query to know if the document has been fully serialised by testing whether the root has a archimate:fragment property. If it has, the algorithm has reached the final level of the document.
        resultquery = serializable_graph.query('''
            
        PREFIX archiXML: <https://data.rijksfinancien.nl/archixml/model/def/>                                               
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xml: <http://www.w3.org/XML/model/def/> 


        ASK 
        WHERE {
          ?document a archiXML:Document ;
                  xml:fragment ?fragment.
        }

        ''')   

        # Check whether another iteration is needed. If the archimate root of the document contains a archimate:fragment statement then the serialisation is considered done.
        for result in resultquery:
            if result == False:
                "...not yet fully serialised. Running another SHACL iteration..."
                writeGraph(serializable_graph)
                iteratePyShacl(vocabulary, serializable_graph)
            else: 
                print ("Document is serialised.")
                writeGraph(serializable_graph)
             

# Get the Archimate vocabulary and place it in a string
archimate_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/archiXML - core.ttl")
dom_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/dom - core.ttl")
xml_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/xml - core.ttl")
xmlns_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/xmlns - core.ttl")
xlink_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/xlink - core.ttl")
xsi_vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/xsi - core.ttl")

vocabulary = archimate_vocabulary + '\n' + dom_vocabulary + '\n' + xml_vocabulary + '\n' + xmlns_vocabulary + '\n' + xlink_vocabulary + '\n' + xsi_vocabulary

# loop through any turtle files in the input directory
for filename in os.listdir(directory_path+"/OntoArchimate/Tools/ArchiXML2Archimate/Input"):
    if filename.endswith(".ttl"):
        file_path = os.path.join(directory_path+"/OntoArchimate/Tools/ArchiXML2Archimate/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # Get the RDF-model of some Archimate document and place it in a string. 
        document_graph = readGraphFromFile(file_path)                  

        # Join the Archimate vocabulary and the RDF-model of some Archimate document into a string
        serializable_graph_string = vocabulary + document_graph

        # Create a graph of the string containing the Archimate vocabulary and the RDF-model of some Archimate document
        serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="ttl")

        # Inform user
        print ("Serialising Archimate data as contained in document '" + filename + "'...")

        # Call the shacl engine with the Archimate vocabulary and the document to be serialized
        iteratePyShacl(xml_vocabulary, serializable_graph)

        # Prepare a graph to query the serialized document
        serialized_graph = rdflib.Graph().parse(directory_path+"/OntoArchimate/Tools/ArchiXML2Archimate/Output/"+filename_stem+"-serialized.ttl" , format="ttl")

        # Query to get the resulting fragment of the document
        documentQuery = serialized_graph.query('''

        PREFIX archiXML: <https://data.rijksfinancien.nl/archixml/model/def/>                                               
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xml: <http://www.w3.org/XML/model/def/> 


        select ?fragment
        WHERE {
          ?document a archiXML:Document ;
                  xml:fragment ?fragment.
        }

        ''')   

        # Write serialized html to actual html file
        for result in documentQuery:
            with open(directory_path+"/OntoArchimate/Tools/ArchiXML2Archimate/Output/"+filename_stem+"-serialized.xml", 'w', encoding='utf-8') as file:
               file.write(result.fragment)
               print ("\nDocument is saved to Archimate-format as " + filename_stem+"-serialized.xml")

  

