from pylila.sparql import query
from rdflib import Graph, URIRef
import logging


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
        self.uri = URIRef(uri)
        self.graph = Graph()
        self.load_graph()

    @property
    def writter_representations(self):
        pass

    def load_graph(self):
        q = '''CONSTRUCT { <%s> ?p ?o } where {
                <%s> ?p ?o }''' % (str(self.uri), str(self.uri))
        res = query(q, out_format='ttl')
        if res.status_code != 200:
            logging.error(f"Server returned status: {res.status_code}")
            return None
        self.graph.parse(data=res.text)
