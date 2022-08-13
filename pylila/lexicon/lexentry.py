import logging
from pylila.sparql import query
from rdflib import Graph, URIRef
from pylila.resources import LiLaRes
from pylila.urirefs import (ontolex, lila, canonical_form)


class LexicalEntry(LiLaRes):
    def __init__(self, uri, graph=None):
        super().__init__(self._validate_uri(uri), graph=graph)

    @property
    def lemma(self):
        lms = self._get_objects_from_graph(canonical_form)
        if not lms:
            logging.error("This Lexical Entry is not linked to a Canonical Form")
        return lms

    @property
    def senses(self):
        return self._get_objects_from_graph(ontolex.sense)

    @property
    def concepts(self):
        return self._get_objects_from_graph(ontolex.evokes)

    def get_forms(self, obj_property=ontolex.otherForm):
        return self._get_objects_from_graph(obj_property)

    def get_concepts_and_definitions(self, concepts=None):
        if not concepts:
            concepts = self.concepts
        if type(concepts) == str:
            concepts = [concepts]
        cps = [f'<{lc}>' for lc in concepts]
        nl = '\n'
        q = f'''PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                select ?lc ?def where {{
                  VALUES ?lc {{ {nl.join(cps)}
                }}
                ?lc skos:definition ?def
                }}
        '''
        res = query(q)
        defs = [(r['lc']['value'], r['def']['value']) for r in res.json()['results']['bindings'] ]
        return defs

    def get_lexicons(self):
        """
        Every Lexical Entry in LiLa belongs to at least one lime:Lexicon.
        Get the list of the lexicons

        :return: The URI(s) of the connected Lexicon(s)
        :rtype: tuple of rdflib.term.URIRef
        """
        q = f'''PREFIX lime: <http://www.w3.org/ns/lemon/lime#>
               SELECT ?lexres where {{ ?lexres lime:entry <{str(self.uri)}> . }}
            '''
        return self._get_uris_from_sparql(q, 'lexres')

    @staticmethod
    def _validate_uri(uri):
        if uri.startswith('https://lila-erc.eu/'):
            return uri.replace('https://', 'http://')
        return uri
