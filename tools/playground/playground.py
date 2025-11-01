from flask import Flask, request, render_template, url_for
import rdflib
from rdflib import Graph, Namespace, Literal, RDF, Dataset
import pyshacl
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import os

app = Flask(__name__, template_folder='tools/playground/templates', static_folder='tools/playground/static')

# Get the current working directory in which the Playground.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir))

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
    graph.serialize(destination=directory_path + "/tools/playground/" + name + ".trig", format="trig")
    
# Function to read a graph (as a string) from a file 
def readStringFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content


# Get all the vocabularies and place them in a string
dom_vocabulary          = readStringFromFile(directory_path + "/specification/dom - core.trig")
xml_vocabulary          = readStringFromFile(directory_path + "/specification/xml - core.trig")
xmlns_vocabulary        = readStringFromFile(directory_path + "/specification/xmlns - core.trig")
xlink_vocabulary        = readStringFromFile(directory_path + "/specification/xlink - core.trig")
xsi_vocabulary          = readStringFromFile(directory_path + "/specification/xsi - core.trig")
svg_vocabulary          = readStringFromFile(directory_path + "/specification/svg - core.trig")
rdfa_vocabulary         = readStringFromFile(directory_path + "/specification/rdfa - core.trig")
archimate_vocabulary    = readStringFromFile(directory_path + "/specification/archimate - core.trig")
archiXML_vocabulary     = readStringFromFile(directory_path + "/specification/archiXML - core.trig")
archiSVG_vocabulary     = readStringFromFile(directory_path + "/specification/archiSVG - core.trig")
archimate_serialisation = readStringFromFile(directory_path + "/specification/archimate - serialisation.trig")
archiXML_serialisation  = readStringFromFile(directory_path + "/specification/archiXML - serialisation.trig")
archiSVG_serialisation  = readStringFromFile(directory_path + "/specification/archiSVG - serialisation.trig")

vocabulary = dom_vocabulary + '\n' + xml_vocabulary + '\n' + xmlns_vocabulary + '\n' + xlink_vocabulary + '\n' + xsi_vocabulary + '\n' + archimate_vocabulary + '\n' + archiXML_vocabulary + '\n' + archiSVG_vocabulary + '\n' + svg_vocabulary + '\n' + rdfa_vocabulary + '\n'
example_rdf_code = readStringFromFile(directory_path + "/examples/ArchimateBasicModel.trig")
example_archimate_code = readStringFromFile(directory_path + "/examples/ArchimateBasicModel.xml")


def generate_element_id(element):
    # Base case: If there's no parent, return an empty string (root-level element)
    if element.parent is None:
        return "1"

    # Initialize the sibling index for the current element
    sibling_index = 1
    # Count previous siblings (including text and non-element nodes)
    for sibling in element.previous_siblings:
        sibling_index += 1

    # Recursive call: Get the parent's ID
    parent_id = generate_element_id(element.parent)

    # If the parent ID is not empty, append the current element's sibling index
    if parent_id:
        return f"{parent_id}.{sibling_index}"
    else:
        return str(sibling_index)  # This happens at the root level

def transform2ArchiVoc(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the Archimate serialization vocabulary to the Archimate model
        old_triples = set(serializable_graph.quads((None, None, None, None)))

        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
              
        new_triples = set(serializable_graph.quads((None, None, None, None)))

        # If new triples were added, recurse
        if new_triples != old_triples:
           print("transform2ArchiVoc iteration - running")
           return transform2ArchiVoc(shaclgraph, serializable_graph)
        else:
           print("transform2ArchiVoc - done")              
           return serializable_graph
            
def transform2ArchiXML(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the ArchiXML vocabulary to the Archimate model
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        # Query to know if the model has been fully transformed by testing whether all archimate concepts in the model have a archiXML mirror element. 
        resultquery = serializable_graph.query('''

        PREFIX archimate: <https://data.rijksfinancien.nl/archimate/model/def/>
        PREFIX archiXML:  <https://data.rijksfinancien.nl/archixml/model/def/>
        PREFIX prov:      <http://www.w3.org/ns/prov#>
        PREFIX rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:      <http://www.w3.org/2000/01/rdf-schema#>       
        PREFIX xml:       <http://www.w3.org/XML/model/def/> 

        ASK 
        WHERE {
          ?concept rdf:type/rdfs:subClassOf* archimate:Concept.
          
          # Do not check Archimate concepts themselves
          filter not exists {
          ?concept rdfs:isDefinedBy archimate:.
          }
          
          # Are there any unprocessed Archimate model concepts?
          filter not exists {
          ?archiXML prov:wasDerivedFrom ?concept;
                   rdf:type/rdfs:subClassOf* archiXML:DomElement.
          }            
        }

        ''')   

        # Check whether another iteration is needed. 
        for result in resultquery:
            print("transform2ArchiXML iteration - running")
            if result == True:
                return transform2ArchiXML(shaclgraph, serializable_graph)
            else:
                print("transform2ArchiXML - done")                
                return serializable_graph

def transform2ArchiSVG(shaclgraph, serializable_graph, iterator):
        
        old_triples = set(serializable_graph.quads((None, None, None, None)))  
        
        # call PyShacl engine and apply the ArchiSVG vocabulary to the Archimate model
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        new_triples = set(serializable_graph.quads((None, None, None, None)))

        # If new triples were added, recurse
        if new_triples != old_triples:
           print("transform2ArchiSVG iteration - running")
           return transform2ArchiSVG(shaclgraph, serializable_graph, iterator)
        elif iterator < 10:          
           print("transform2ArchiSVG iteration - finalizing")            
           iterator = iterator + 1
           return transform2ArchiSVG(shaclgraph, serializable_graph, iterator)
        else:
            print("transform2ArchiSVG maximum iterations done")  
            return serializable_graph                        
            
def serializeXMLFragment(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the Archimate vocabulary to the serializable Archimate document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="trig",
        shacl_graph_format="trig",
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
            print ("check if fragment is complete: ", result)
            if result == False:
                return serializeXMLFragment(shaclgraph, serializable_graph)
         
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

def serializeSVGFragment(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the ArchiSVG vocabulary to the serializable Archimate document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        # Query to know if the document has been fully serialised by testing whether the root has a xml:fragment property. If it has, the algorithm has reached the final level of the document.
        resultquery = serializable_graph.query('''
                                               
prefix archimate: <https://data.rijksfinancien.nl/archimate/model/def/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs:      <http://www.w3.org/2000/01/rdf-schema#>
prefix svg:       <http://www.w3.org/SVG/model/def/>
prefix xml:       <http://www.w3.org/XML/model/def/>

ask
where {
  ?document a svg:Document ;
    prov:wasDerivedFrom ?archimateView;
    xml:fragment ?fragment.
  ?archimateModel rdf:type archimate:View.
}

        ''')   

        # Check whether another iteration is needed. If the archimate root of the document contains a xml:fragment statement then the serialisation is considered done.
        for result in resultquery:
            print ("check if fragment is complete: ", result)
            if result == False:
                return serializeSVGFragment(shaclgraph, serializable_graph)
         
            else:
                xmlQuery = serializable_graph.query('''
                   
prefix archimate: <https://data.rijksfinancien.nl/archimate/model/def/>
prefix prov: <http://www.w3.org/ns/prov#>
prefix rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs:      <http://www.w3.org/2000/01/rdf-schema#>
prefix svg:       <http://www.w3.org/SVG/model/def/>
prefix xml:       <http://www.w3.org/XML/model/def/>

select ?fragment
where {
  ?document a svg:Document ;
    prov:wasDerivedFrom ?archimateView;
    xml:fragment ?fragment.
  ?archimateModel rdf:type archimate:View.
}
               ''')   

         
                for xml in xmlQuery:
                    print ("xml.fragment = ", xml.fragment)
                    return xml.fragment

@app.route('/convert2Archimate', methods=['POST'])
def convert_to_archimate():
    try:
        print("Converting RDF to XML...")    
        print("Step 1: transforming archimate vocabulary to archiXML...")    
        text = request.form['rdf']   
        g = Dataset(default_union=True)
        g.parse(data=text , format="trig")
        # Zet de RDF-triples om naar een string
        triples = g.serialize(format='trig')
        serializable_graph_string = vocabulary + triples
        serializable_graph = Dataset(default_union=True)
        serializable_graph.parse(data=serializable_graph_string , format="trig")    
        serializable_graph = transform2ArchiXML(archiXML_serialisation, serializable_graph)  
        print("Step 2: serializing archiXML to XML code")     
        archimate_fragment = serializeXMLFragment(xml_vocabulary, serializable_graph)
        filepath = directory_path+"/tools/playground/static/output.xml"
        with open(filepath, 'w', encoding='utf-8') as file:
           file.write(archimate_fragment)    
        writeGraph(serializable_graph, "static/output")
        return render_template('index.html', xmlRawOutput=archimate_fragment, rdfInput=text, rdfOutputButton="true")

    except Exception as e:
        print("Error during processing:", e)
        return render_template('index.html', rdfInput=f"Error: {e}")

@app.route('/convert2SVG', methods=['POST'])
def convert_to_SVG():
    try:
        print("Converting RDF to SVG...")    
        print("Step 1: transforming archimate vocabulary to archiSVG...")  
        text = request.form['rdf']   
        g = Dataset(default_union=True)
        g.parse(data=text , format="trig")
        # Zet de RDF-triples om naar een string
        triples = g.serialize(format='trig')
        serializable_graph_string = vocabulary + triples
        serializable_graph = Dataset(default_union=True)
        serializable_graph.parse(data=serializable_graph_string , format="trig")
        
        serializable_graph = transform2ArchiSVG(archiSVG_serialisation, serializable_graph, 1)   
        print("Step 2: serializing archiSVG to SVG code...")      
        svg_fragment = serializeSVGFragment(xml_vocabulary, serializable_graph)
        filepath = directory_path+"/tools/playground/static/output.xml"
        src_filepath = url_for('static', filename='output.xml')
        with open(filepath, 'w', encoding='utf-8') as file:
           file.write(svg_fragment)
        writeGraph(serializable_graph, "static/output")
        return render_template('index.html', xmlRawOutput=svg_fragment, rdfInput=text, htmlOutput='<iframe src='+ src_filepath + ' width="100%" height="600"></iframe>', rdfOutputButton="true")

    except Exception as e:
        print("Error during processing:", e)
        return render_template('index.html', rdfInput=f"Error: {e}")
    
@app.route('/convert2RDF', methods=['POST'])
def convert_to_rdf():
    try:
        print("Converting XML to RDF...")
        print("Step 1: parsing XML into ArchiXML...")
        archimateInput = request.form['archimate']
        # initialize graph
        g = Dataset(default_union=True)
              
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)
        g.bind("archiXML", archiXML)
        g.bind("archimate", archimate)        
        g.bind("xml", xml)
        g.bind("xmlns", xmlns)
        g.bind("xlink", xlink)
        g.bind("xsi", xsi)        

        # fill graph with archiXML vocabulary
        xml_graph = Dataset(default_union=True)
        xml_graph.parse(directory_path+"/specification/archiXML - core.trig" , format="trig")

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
                        elif namespace == 'xsi':
                            namespace_uri = xsi                            
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
                      g.add((doc[child_id], RDF.type, archiXML["Text"]))
                      
                      # empty content (of type None) in html needs to be converted to empty string
                      if element.string == None: 
                          text_fragment = "" 
                      else:
                          text_fragment = element.string
                      
                      # write string content of the text element to the graph
                      g.add((doc[child_id], xml["fragment"], Literal(text_fragment)))

        # return the resulting triples
        print("Step 2: transforming archiXML to archimate vocabulary...")            
        archiXMLTriples = g.serialize(format="trig")
        serializable_graph_string = vocabulary + '\n' + archiXMLTriples + '\n'
        serializable_graph = Dataset(default_union=True)
        serializable_graph.parse(data=serializable_graph_string , format="trig")    
        serializable_graph = transform2ArchiVoc(archimate_serialisation, serializable_graph)        
        triples = serializable_graph.serialize(format="trig").split('\n')
        writeGraph(serializable_graph, "static/output")
        return render_template('index.html', rdfOutput=triples, xmlRawInput = archimateInput, rdfOutputButton="true")
    
    except Exception as e:
        print("Error during processing:", e)
        return render_template('index.html', xmlRawInput=f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html', rdfInput=example_rdf_code, xmlRawInput=example_archimate_code)

if __name__ == '__main__':
    app.run()
