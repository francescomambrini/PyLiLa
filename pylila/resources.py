import logging
from pylila.sparql import query
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS, RDF


class LiLaRes:
    def __init__(self, uri, graph=None):
        self.uri = URIRef(self._validate_uri(uri))
        if not graph:
            self.graph = Graph()
            self.load_graph()
        else:
            self.graph = graph

    def load_graph(self):
        q = f'''CONSTRUCT {{ <{str(self.uri)}> ?p ?o }} where {{
                <{str(self.uri)}> ?p ?o }}'''
        res = query(q, out_format='ttl')
        if res.text == '# Empty TURTLE\n':
            logging.error(f'Resource not found in LiLa')
            return None
        self.graph.parse(data=res.text)

    def get_inverse_graph(self):
        q = f'''CONSTRUCT {{ ?s ?p <{str(self.uri)}> }} where {{
                        ?s ?p <{str(self.uri)}> }}'''
        res = query(q, out_format='ttl')
        if res.text == '# Empty TURTLE\n':
            logging.error(f'Resource not found in LiLa')
            return None
        g = Graph()
        return g.parse(data=res.text)

    @property
    def labels(self):
        return self._get_objects_from_graph(RDFS.label)

    @property
    def types(self):
        return self._get_objects_from_graph(RDF.type)

    def _get_objects_from_graph(self, object_uri):
        return tuple([rpr for rpr in self.graph.objects(self.uri, object_uri)])

    def _validate_uri(self, uri):
        if uri.startswith('https://lila-erc.eu/'):
            uri = uri.replace('https://lila-erc.eu/', 'http://lila-erc.eu/')
            logging.debug("Lemma bank URIs use the http protocol, not https!")
        return uri

    def get_label(self):
        """
        Generates a string version of the label. If there's more than one label,
        it joins them with a comma

        :return: label(s) as a string
        :rtype: str
        """
        return self._generate_string_reps(self.labels)

    @staticmethod
    def _generate_string_reps(literals):
        return ', '.join([str(l) for l in literals])

    @staticmethod
    def _get_uris_from_sparql(qstr, colname):
        res = query(qstr)
        return [URIRef(h[colname]['value']) for h in res.json()['results']['bindings']]

    @classmethod
    def from_string(cls, rdf_string):
        g = Graph()
        g.parse(data=rdf_string)
        if len(set(g.subjects(None, None))) > 1:
            logging.warning("Your graph has multiple subjects; I'm picking the first")
        u = list(g.subjects(None, None))[0]
        return cls(u, graph=g)

    @classmethod
    def from_file(cls, rdf_path):
        with open(rdf_path) as f:
            rdf_string = f.read()
        return cls.from_string(rdf_string)
