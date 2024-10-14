from flask import Flask, request, render_template
import rdflib
from rdflib import Graph, Namespace, Literal, RDF
import pyshacl
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import os

app = Flask(__name__)

# Get the current working directory in which the Playground.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir, '..', '..','..'))

# namespace declaration
rdf       = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs      = Namespace("http://www.w3.org/2000/01/rdf-schema#")
doc       = Namespace("https://data.rijksfinancien.nl/archixml/doc/id/")
dom       = Namespace("http://www.w3.org/DOM/model/def/") 
archimate = Namespace("https://data.rijksfinancien.nl/archimate/model/def/")
archiXML  = Namespace("https://data.rijksfinancien.nl/archixml/model/def/")
xml       = Namespace("http://www.w3.org/XML/model/def/")
xmlns     = Namespace("http://www.w3.org/2000/xmlns/model/def/")
xlink     = Namespace("https://www.w3.org/1999/xlink/model/def/")
xsi       = Namespace("http://www.w3.org/2001/XMLSchema-instance/model/def/")

def writeGraph(graph, name):
    graph.serialize(destination=directory_path + "/OntoArchimate/Tools/Playground/" + name + ".ttl", format="turtle")
    
# Function to read a graph (as a string) from a file 
def readStringFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content


# Get all the vocabularies and place them in a string
dom_vocabulary          = readStringFromFile(directory_path + "/OntoArchimate/Specification/dom - core.ttl")
xml_vocabulary          = readStringFromFile(directory_path + "/OntoArchimate/Specification/xml - core.ttl")
xmlns_vocabulary        = readStringFromFile(directory_path + "/OntoArchimate/Specification/xmlns - core.ttl")
xlink_vocabulary        = readStringFromFile(directory_path + "/OntoArchimate/Specification/xlink - core.ttl")
archimate_vocabulary    = readStringFromFile(directory_path + "/OntoArchimate/Specification/archimate - core.ttl")
archiXML_vocabulary     = readStringFromFile(directory_path + "/OntoArchimate/Specification/archiXML - core.ttl")
archimate_serialisation = readStringFromFile(directory_path + "/OntoArchimate/Specification/archimate - serialisation.ttl")
archiXML_serialisation  = readStringFromFile(directory_path + "/OntoArchimate/Specification/archiXML - serialisation.ttl")

vocabulary = dom_vocabulary + '\n' + xml_vocabulary + '\n' + xmlns_vocabulary + '\n' + xlink_vocabulary + '\n' + archiXML_vocabulary + '\n'
example_rdf_code = readStringFromFile(directory_path + "/OntoArchimate/Examples/ArchiXMLBasicModel.ttl")
example_archimate_code = readStringFromFile(directory_path + "/OntoArchimate/Examples/ArchimateBasicModel.xml")


def generate_element_id(element):
    # generate an identifier for an element in the xml
    parent_string = ""
    for parent in element.parents:
        parent_sibling_count = 0
        for parent_sibling in parent.previous_siblings:    
            parent_sibling_count = parent_sibling_count + 1
        horizontal_parental_index = parent_sibling_count
        if parent.name:
            parent_string = parent_string + str(horizontal_parental_index)
        else:
            parent_string = parent_string + "0"
        
    count_sibling = 0
    for sibling in element.previous_siblings:    
        count_sibling = count_sibling + 1
    horizontal_index = count_sibling
    
    element_id = f"{parent_string}/{horizontal_index}" 
    
    return element_id.replace("[document]/","")

def iteratePyShacl(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the Archimate vocabulary to the serializable Archimate document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        # Query to know if the document has been fully serialised by testing whether the root has a xml:fragment property. If it has, the algorithm has reached the final level of the document.
        resultquery = serializable_graph.query('''
            
        PREFIX rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:      <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX archiXML:  <https://data.rijksfinancien.nl/archixml/model/def/>
        PREFIX xml:       <http://www.w3.org/XML/model/def/> 

        ASK 
        WHERE {
          ?document a archiXML:Document ;
                  xml:fragment ?fragment.
        }

        ''')   

        # Check whether another iteration is needed. If the archimate root of the document contains a xml:fragment statement then the serialisation is considered done.
        for result in resultquery:
            print ("ask result = ", result)
            if result == False:
                writeGraph(serializable_graph, 'TEST')
                return iteratePyShacl(shaclgraph, serializable_graph)
         
            else:
                xmlQuery = serializable_graph.query('''
                   
        PREFIX rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:      <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX archiXML:  <https://data.rijksfinancien.nl/archixml/model/def/>
        PREFIX xml:       <http://www.w3.org/XML/model/def/> 

               select ?fragment
               WHERE {
                 ?document a archiXML:Document ;
                  xml:fragment ?fragment.
               }

               ''')   

         
                for xml in xmlQuery:
                    print ("xml.fragment = ", xml.fragment)
                    return xml.fragment


@app.route('/convert2Archimate', methods=['POST'])
def convert_to_archimate():
    text = request.form['rdf']   
    g = rdflib.Graph().parse(data=text , format="turtle")
    # Zet de RDF-triples om naar een string
    triples = g.serialize(format='turtle')
    serializable_graph_string = vocabulary + '\n' + triples
    serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="turtle")
    archimate_fragment = iteratePyShacl(xml_vocabulary, serializable_graph)
    print("Archimate fragment =", archimate_fragment)
    return render_template('index.html', xmlRawOutput=archimate_fragment, rdfInput=text)

@app.route('/convert2RDF', methods=['POST'])
def convert_to_rdf():
        archimateInput = request.form['archimate']
        # initialize graph
        g = Graph(bind_namespaces="rdflib")
              
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)
        g.bind("archiXML", archiXML)
        g.bind("archimate", archimate)        
        g.bind("xml", xml)
        g.bind("xmlns", xmlns)
        g.bind("xlink", xlink)

        # fill graph with archiXML vocabulary
        xml_graph = Graph().parse(directory_path+"/OntoArchimate/Specification/archiXML - core.ttl" , format="ttl")

        # string for query to establish IRI of a 'tag' HTML element
        tagquerystring = '''
            
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix xml: <http://www.w3.org/XML/model/def/>

        select ?element_IRI where {
          ?element_IRI xml:tag ?tag
        }
        '''

        # parse xml document
        soup = BeautifulSoup(archimateInput, features="xml")
        root_element = soup.contents[0]
        root_id = generate_element_id(root_element)
       
        # loop through each element in the XML document
        for element in soup.descendants:
            # check if the element is an XML tag element
            if isinstance(element, Tag):
                # establish unique id for the XML tag element
                element_id = generate_element_id(element)
                
                # establish IRI for the tag class based on the XML vocabulary
                tag_result = xml_graph.query(tagquerystring, initBindings={"tag" : Literal(element.name)})
                for row in tag_result:
                    tag_IRI = row.element_IRI
                    
                # add the element to the graph with its unique identifier as IRI and its tag as type
                g.add((doc[element_id], RDF.type, tag_IRI))
                
                # add a document node as a container of the XML-tree
                if element.name == 'model':
                    document_id = '1'
                    g.add((doc[document_id], RDF.type, archiXML["Document"]))
                    g.add((doc[document_id], rdf["_" + str(document_id)], doc[element_id]))
        
                # establish optional attributes of the element
                for attribute, values in element.attrs.items():
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
                        elif namespace == 'xmlns':
                            namespace_uri = xmlns
                        elif namespace == 'archimate':
                            namespace_uri = archimate
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
                        # Add optional attributes of the element to the graph
                        g.add((doc[element_id], namespace_uri[local_name], Literal(attribute_value)))
                    
                # go through the direct children of the element
                member_count = 0 # initialize count
                for child in element.children:
                    member_count = member_count + 1 # count the number of direct children, so that we can establish the sequence of appearance of the children within the parent element, through the 'rdf:_x' property between parent and child.
                    
                    # if the child is an xml tag element get its unique identifier based on sourceline and sourcepos
                    if isinstance(child, Tag):
                      if child.name == None  :
                          childname = ""
                      else:
                          childname = child.name
                      child_id = generate_element_id(child)
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))
                      
                    # if the child is an text element, create a unique identifier based on sourceline and sourcepos of its parent and the sequence position of the child within the parent, as the html-parser does not have sourceline and sourcepos available as attributes for text elements.
                    elif isinstance(child, NavigableString):
                      if child.name == None  :
                            childname = "Text"
                      else:
                            childname = child.name
                      child_id = generate_element_id(child)
                      
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child element is of type TextElement
                      g.add((doc[child_id], RDF.type, archimate["Text"]))
                      
                      # empty content (of type None) in html needs to be converted to empty string
                      if element.string == None: 
                          text_fragment = "" 
                      else:
                          text_fragment = element.string
                      
                      # write string content of the text element to the graph
                      g.add((doc[child_id], xml["fragment"], Literal(text_fragment)))

        # return the resulting triples
        triples = g.serialize(format="turtle").split('\n')
        return render_template('index.html', rdfOutput=triples, xmlRawInput = archimateInput)

@app.route('/')
def index():
    return render_template('index.html', rdfInput=example_rdf_code, xmlRawInput=example_archimate_code)

if __name__ == '__main__':
    app.run()
