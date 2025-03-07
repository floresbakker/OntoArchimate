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
    graph.serialize(destination=directory_path+"/OntoArchimate/Tools/ArchiXML2ArchiVoc/Output/"+filename_stem+"-serialized.ttl", format="turtle")

# Function to call the PyShacl engine so that a RDF model of a Archimate document can be serialized to Archimate-code.
def iteratePyShacl(vocabulary, serializable_graph):
        
        # call PyShacl engine and apply the Archimate vocabulary to the serializable Archimate document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=vocabulary,
        data_graph_format="ttl",
        shacl_graph_format="ttl",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        writeGraph(serializable_graph)                                    
               

# Get the Archimate vocabulary and place it in a string
vocabulary = readGraphFromFile(directory_path + "/OntoArchimate/Specification/archimate - core.ttl")
serialisation = readGraphFromFile(directory_path + "/OntoArchimate/Specification/archimate - serialisation.ttl")


# loop through any turtle files in the input directory
for filename in os.listdir(directory_path+"/OntoArchimate/Tools/ArchiXML2ArchiVoc/Input"):
    if filename.endswith(".ttl"):
        file_path = os.path.join(directory_path+"/OntoArchimate/Tools/ArchiXML2ArchiVoc/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # Get the RDF-model of some Archimate document and place it in a string. 
        document_graph = readGraphFromFile(file_path)                  

        # Join the Archimate vocabulary and the RDF-model of some Archimate document into a string
        serializable_graph_string = vocabulary + document_graph

        # Create a graph of the string containing the Archimate vocabulary and the RDF-model of some Archimate document
        serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="turtle")

        # Inform user
        print ("\nTransforming archiXML model to an archimate model as contained in document '" + filename + "'...")

        # Call the shacl engine with the Archimate vocabulary and the document to be serialized
        iteratePyShacl(serialisation, serializable_graph)
        

    
