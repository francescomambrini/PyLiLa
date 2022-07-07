import logging
from pylila.sparql import query
from rdflib import Graph, URIRef
from pylila.urirefs import (written_rep, lila)


def get_all_lemmas(output_format):
    q = '''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            select ?lemma {
              { ?lemma a lila:Lemma }
              union
              { ?lemma a lila:Hypolemma }
        }'''
    lms = query(q, output_format)


def get_lemmas_by_writtenrep(lemma_string):
    spql = '''PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
    SELECT ?lemma where {
       ?lemma ontolex:writtenRep "%s"
    }
    ''' % lemma_string
    res = query(spql)
    if res:
        return [r['lemma']['value'] for r in res.json()['results']['bindings']]
    else:
        return []


def _validate_lemma_uri(uri):
    lb_base = 'http://lila-erc.eu/data/id/lemma/'
    if uri.isnumeric():
        uri = lb_base + uri
        logging.debug("Replaced numeric ID with full http URI for lemmas (doesn't work with hypo's)")
    if uri.startswith('https://lila-erc.eu/'):
        uri = uri.replace('https://lila-erc.eu/', 'http://lila-erc.eu/')
        logging.debug("Lemma bank URIs use the http protocol, not https!")
    return uri


class Lemma:
    def __init__(self, uri):
        uri = _validate_lemma_uri(uri)
        self.uri = URIRef(uri)
        self.graph = Graph()
        self.load_graph()

    @property
    def written_representations(self):
        return tuple([str(rpr) for rpr in self.graph.objects(self.uri, written_rep)])

    @property
    def lexical_bases(self):
        return tuple([str(b) for b in self.graph.objects(self.uri, lila.hasBase)])

    @property
    def prefixes(self):
        return tuple([str(p) for p in self.graph.objects(self.uri, lila.hasPrefix)])

    @property
    def suffixes(self):
        return tuple([str(p) for p in self.graph.objects(self.uri, lila.hasSuffix)])

    @property
    def lemma_variants(self):
        return tuple([str(lv) for lv in self.graph.objects(self.uri, lila.lemmaVariant)])

    @property
    def pos(self):
        pos = [p for p in self.graph.objects(self.uri, lila.hasPOS)]
        if len(pos) > 1:
            logging.error(f"{self.uri} has more than one POS!")
        elif len(pos) == 0:
            logging.error(f"{self.uri} has no POS!")
            return None
        return str(pos[0])

    @property
    def inflection_type(self):
        it = [p for p in self.graph.objects(self.uri, lila.hasInflectionType)]
        if len(it) > 1:
            logging.warning(f"{self.uri} has more than one Inflection Type!")
        elif len(it) == 0:
            logging.warning(f"{self.uri} has no Inflection Type!")
            return None
        return str(it[0])

    def get_hypolemmas(self):
        q = '''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            SELECT ?hypo where { ?hypo   lila:isHypolemma <%s> . }
        ''' % str(self.uri)
        return self._get_uris_from_sparql(q, 'hypo')

    def get_lexical_entries(self):
        q = '''PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
               SELECT ?lexentry where { ?lexentry ontolex:canonicalForm <%s> . }
            ''' % str(self.uri)
        return self._get_uris_from_sparql(q, 'lexentry')

    def get_tokens(self):
        q = '''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            SELECT ?tok where { ?tok lila:hasLemma <%s> . }
            ''' % str(self.uri)
        return self._get_uris_from_sparql(q, 'tok')

    def load_graph(self):
        q = '''CONSTRUCT { <%s> ?p ?o } where {
                <%s> ?p ?o }''' % (str(self.uri), str(self.uri))
        res = query(q, out_format='ttl')
        if not res:
            logging.error(f'Lemma not found in the Lemma Bank')
            return None
        self.graph.parse(data=res.text)

    @staticmethod
    def _get_uris_from_sparql(qstr, colname):
        res = query(qstr)
        return [h[colname]['value'] for h in res.json()['results']['bindings']]
