from SPARQLWrapper import SPARQLWrapper, JSON, XML, CSV, TURTLE
import logging

LILA_SPARQL_URL = "https://lila-erc.eu/sparql/lila_knowledge_base/sparql"


def query(query_string, out_format='json'):
    dic_out = {'json': JSON, 'xml': XML, 'ttl': TURTLE, 'turtle': TURTLE, 'csv': CSV}
    sparql = SPARQLWrapper(LILA_SPARQL_URL)
    try:
        sparql.setReturnFormat(dic_out[out_format])
    except KeyError:
        raise ValueError(f"Outpout format must be one of: {', '.join(dic_out.keys())}")

    sparql.setQuery(query_string)
    try:
        ret = sparql.queryAndConvert()
    except Exception as e:
        logging.error(e)
        return None
    return ret

