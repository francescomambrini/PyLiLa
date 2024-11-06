import logging
from pylila.sparql import query
from pylila.resources import LiLaRes
from rdflib import Graph, URIRef
from pylila.urirefs import (written_rep, lila)
from pylila.pos import upos_lila_mapping


def get_all_lemmas(output_format, include_hypolemmas=True):
    q = '''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            select ?lemma {
              { ?lemma a lila:Lemma }              
        '''
    if include_hypolemmas:
        q += '''union
              { ?lemma a lila:Hypolemma }
              '''
    q += '}'
    lms = query(q, output_format)
    return lms


def get_lemmas_by_writtenrep(lemma_string):
    spql = f'''PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
    SELECT ?lemma where {{
       ?lemma ontolex:writtenRep "{lemma_string}"@la
    }}
    '''
    res = query(spql)
    if res:
        return [r['lemma']['value'] for r in res.json()['results']['bindings']]
    else:
        return []
    
def get_lemmas_by_writtenrep_upos(lemma_string, upos):
    pos = upos_lila_mapping.get(upos, 'http://lila-erc.eu/ontologies/lila/other') 
    spql = f'''PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
    PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
    SELECT ?lemma where {{
       ?lemma ontolex:writtenRep "{lemma_string}" ;
            lila:hasPOS <{pos}>
    }}
    '''
    res = query(spql)
    if res:
        return [r['lemma']['value'] for r in res.json()['results']['bindings']]
    else:
        return []


class Lemma(LiLaRes):
    # def __init__(self, uri, graph=None):
    #     super().__init__(_validate_lemma_uri(uri), graph=graph)

    @property
    def written_representations(self):
        """
        The Lemma's Written representations

        :return: a tuple of written representations
        :rtype: tuple of rdflib.Literal
        """
        return tuple([rpr for rpr in self.graph.objects(self.uri, written_rep)])

    @property
    def lexical_bases(self):
        return self._get_objects_from_graph(lila.hasBase)

    @property
    def prefixes(self):
        return self._get_objects_from_graph(lila.hasPrefix)

    @property
    def suffixes(self):
        return self._get_objects_from_graph(lila.hasSuffix)

    @property
    def lemma_variants(self):
        return self._get_objects_from_graph(lila.lemmaVariant)

    @property
    def pos(self):
        pos = [p for p in self.graph.objects(self.uri, lila.hasPOS)]
        if len(pos) > 1:
            logging.error(f"{self.uri} has more than one POS!")
        elif len(pos) == 0:
            logging.error(f"{self.uri} has no POS!")
            return None
        return pos[0]

    @property
    def inflection_type(self):
        it = [p for p in self.graph.objects(self.uri, lila.hasInflectionType)]
        if len(it) > 1:
            logging.warning(f"{self.uri} has more than one Inflection Type!")
        elif len(it) == 0:
            logging.warning(f"{self.uri} has no Inflection Type!")
            return None
        return it[0]

    def _validate_uri(self, uri, l_type='lemma'):
        lb_base = f'http://lila-erc.eu/data/id/{l_type}/'
        if str(uri).isnumeric():
            uri = lb_base + str(uri)
            logging.debug("Replaced numeric ID with full http URI for lemmas (doesn't work with hypo's)")

        uri = super()._validate_uri(uri)

        return uri

    def get_written_representations(self):
        """
        Generates a string version of the Lemma's written representations. If there's more than one written rep,
        it joins them with a comma

        :return: written representation(s) as a string
        :rtype: str
        """
        return self._generate_string_reps(self.written_representations)

    def get_hypolemmas(self):
        q = f'''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            SELECT ?hypo where {{ ?hypo   lila:isHypolemma <{str(self.uri)}> . }}
        '''
        return self._get_uris_from_sparql(q, 'hypo')

    def _get_lemmas_from_same_affixes(self, affix_type):
        if affix_type.lower() == 'prefix':
            p = 'lila:hasPrefix'
        elif affix_type.lower() == 'suffix':
            p = 'lila:hasSuffix'
        elif affix_type.lower() == 'base':
            p = 'lila:hasBase'
        else:
            raise ValueError(f"Type must be one of (prefix, suffix, base); got: {affix_type}")
        q = f'''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
        select ?l where {{ 
          <{str(self.uri)}> {p}/^{p} ?l 
          filter(?l != <{str(self.uri)}>)
        }}'''
        return self._get_uris_from_sparql(q, 'l')

    def get_lemmas_from_same_bases(self):
        return self._get_lemmas_from_same_affixes(affix_type='base')

    def get_lemmas_from_same_prefixes(self):
        return self._get_lemmas_from_same_affixes('prefix')

    def get_lemmas_from_same_suffixes(self):
        return self._get_lemmas_from_same_affixes('suffix')

    def get_lexical_entries(self):
        q = f'''PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
               SELECT ?lexentry where {{ ?lexentry ontolex:canonicalForm <{str(self.uri)}> . }}
            '''
        return self._get_uris_from_sparql(q, 'lexentry')

    def get_tokens(self):
        """
        Retrieves the URIs of all tokens (from all corpora) connected to the lemma.
        Returns an empty list if no match is found.

        :return: list of Token URIs, or empty list
        :rtype: list of rdflib.terms.URIRef
        """
        q = f'''PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            SELECT ?tok where {{ ?tok lila:hasLemma <{str(self.uri)}> . }}
            '''
        return self._get_uris_from_sparql(q, 'tok')


class Hypolemma(Lemma):
    
    def _validate_uri(self, uri, l_type='hypolemma'):
        return super(Hypolemma, self)._validate_uri(uri, l_type)
    
    def get_hyperlemma(self):
        pass