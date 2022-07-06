from rdflib import Namespace, URIRef
from rdflib.namespace import DC, RDF, RDFS, DCTERMS

# Namespaces
marl = Namespace('http://www.gsi.dit.upm.es/ontologies/marl/ns#')
lila = Namespace('http://lila-erc.eu/ontologies/lila/')
lime = Namespace('http://www.w3.org/ns/lemon/lime#')
lemonety = Namespace('http://lari-datasets.ilc.cnr.it/lemonEty#')
lila_corpora = Namespace('http://lila-erc.eu/ontologies/lila_corpora/')
ontolex = Namespace("http://www.w3.org/ns/lemon/ontolex#")
olia = Namespace("http://purl.org/olia/olia.owl#")
powla = Namespace('http://purl.org/powla/powla.owl#')

### URIRefs

# properties
written_rep = ontolex.writtenRep
has_lemma = lila.hasLemma
has_string_value = powla.hasStringValue

# classes
lexical_entry = ontolex.LexicalEntry
terminal = powla.Terminal
