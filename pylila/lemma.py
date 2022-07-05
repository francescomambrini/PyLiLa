from pylila.sparql import query
from rdflib import Graph, URIRef


def get_all_lemmas(output_format):
    q = '''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            select ?lemma {
              { ?lemma a lila:Lemma }
              union
              { ?lemma a lila:Hypolemma }
        }'''
    lms = query(q, output_format)


class Lemma:
    def __init__(self, uri):
        self.uri = uri
        self.graph = Graph()

    def load_graph(self):
        q = '''select ?p ?o where {
        <%s> ?p ?o
        }''' % self.uri
