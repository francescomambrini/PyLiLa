from pylila.urirefs import (powla, has_string_value, has_lemma)
from pylila.resources import LiLaRes


class Token(LiLaRes):
    def __init__(self, uri, graph=None):
        super().__init__(uri, graph=graph)

    @property
    def lemma(self):
        return self._get_objects_from_graph(has_lemma)

    @property
    def next(self):
        n = self._get_objects_from_graph(powla.next)
        try:
            return n[0]
        except KeyError:
            return None

    @property
    def previous(self):
        n = self._get_objects_from_graph(powla.previous)
        try:
            return n[0]
        except KeyError:
            return None

    @property
    def string_value(self):
        return ' '.join([str(sv) for sv in self._get_objects_from_graph(has_string_value)])

    def get_annotations(self):
        pass

    def get_sentences(self):
        pass

    def get_deprels(self, rel_direction='both'):
        if rel_direction == 'in':
            prop = "lilaCorpora:hasDep"
        elif rel_direction == 'out':
            prop = 'lilaCorpora:hasHead'
        else:
            prop = 'lilaCorpora:hasDep|lilaCorpora:hasHead'
        q = '''PREFIX lilaCorpora: <http://lila-erc.eu/ontologies/lila_corpora/>
              select ?rel where { ?rel %s <%s> } 
            ''' % (prop, str(self.uri))
        return self._get_uris_from_sparql(q, 'rel')

    def get_document(self):
        q = '''PREFIX lilaCorpora: <http://lila-erc.eu/ontologies/lila_corpora/>
            PREFIX powla: <http://purl.org/powla/powla.owl#>
            select ?doc where {
              <%s> powla:hasLayer/powla:hasDocument ?doc
            }''' % str(self.uri)
        return self._get_uris_from_sparql(q, 'doc')

    def get_corpus(self):
        q = '''PREFIX lilaCorpora: <http://lila-erc.eu/ontologies/lila_corpora/>
            PREFIX powla: <http://purl.org/powla/powla.owl#>
            select ?corpus where {
              <%s> powla:hasLayer/powla:hasDocument/^powla:hasSubDocument ?corpus
            }''' % str(self.uri)
        return self._get_uris_from_sparql(q, 'doc')


class LiLaCorpus(LiLaRes):
    def get_documents(self):
        return self._get_objects_from_graph(powla.hasSubDocument)


class LiLaDocument(LiLaRes):
    def get_tokens(self):
        q = '''PREFIX powla: <http://purl.org/powla/powla.owl#>
            select ?tok where {
              ?layer powla:hasDocument  <%s> ;
                   ^powla:hasLayer ?tok .
              ?tok a powla:Terminal
            }''' % str(self.uri)
        return self._get_uris_from_sparql(q, "tok")
