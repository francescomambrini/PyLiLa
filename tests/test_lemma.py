import unittest
import pylila
from rdflib import Literal
from pylila.lemma import Lemma
import os


LEMMA_GRAPH = '''@prefix lilaLemma:    <http://lila-erc.eu/data/id/lemma/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix lila: <http://lila-erc.eu/ontologies/lila/> .
@prefix ontolex:      <http://www.w3.org/ns/lemon/ontolex#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

lilaLemma:114954  rdf:type      lila:Lemma ;
        rdfs:label              "omnis" ;
        lila:hasBase            <http://lila-erc.eu/data/id/base/2446> ;
        lila:hasDegree          lila:positive ;
        lila:hasInflectionType  lila:n7 ;
        lila:hasPOS             lila:determiner ;
        ontolex:writtenRep      "omnis" .
'''


class TestSum(unittest.TestCase):
    # def setUp(self) -> None:
    #     self.loaded_lemma = Lemma.from_string(LEMMA_GRAPH)
    #     # self.valid_lemma = Lemma('86867')
    #     # self.invalid_lemma = Lemma('bogus')

    def test_loaded_lemma_str(self):
        loaded_lemma = Lemma.from_string(LEMMA_GRAPH)
        self.assertEqual(len(loaded_lemma.graph), 7)
        self.assertEqual(loaded_lemma.written_representations[0], Literal("omnis"))
        self.assertIsInstance(loaded_lemma, Lemma)

    def test_loaded_lemma_file(self):
        fpath = os.path.join(os.path.dirname(pylila.__file__), "../tests/data/lemma.ttl")
        flemma = Lemma.from_file(fpath)
        self.assertEqual(len(flemma.graph), 7)

    # def test_invalid_lemma(self):
    #     l = Lemma('ciccio')
    #     self.assertFalse(len(l.graph) > 0)


if __name__ == '__main__':
    unittest.main()
