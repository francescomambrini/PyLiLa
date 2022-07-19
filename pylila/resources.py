import logging
from pylila.sparql import query
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS, RDF


class LiLaRes:
    def __init__(self, uri):
        self.uri = URIRef(uri)
        self.graph = Graph()
        self.load_graph()

    def load_graph(self):
        q = '''CONSTRUCT { <%s> ?p ?o } where {
                <%s> ?p ?o }''' % (str(self.uri), str(self.uri))
        res = query(q, out_format='ttl')
        if res.text == '# Empty TURTLE\n':
            logging.error(f'Resource not found in LiLa')
            return None
        self.graph.parse(data=res.text)

    @property
    def labels(self):
        return self._get_objects_from_graph(RDFS.label)

    @property
    def types(self):
        return self._get_objects_from_graph(RDF.type)

    def _get_objects_from_graph(self, object_uri):
        return tuple([rpr for rpr in self.graph.objects(self.uri, object_uri)])

    @staticmethod
    def _get_uris_from_sparql(qstr, colname):
        res = query(qstr)
        return [URIRef(h[colname]['value']) for h in res.json()['results']['bindings']]
