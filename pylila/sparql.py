import requests
import logging

LILA_SPARQL_URL = "https://lila-erc.eu/sparql/lila_knowledge_base/sparql"
ACCEPTED_OUT_FORMATS = ['ttl', 'xml', 'json', 'html', 'csv', 'tsv']


def query(query_string, out_format='json'):
    if out_format not in ACCEPTED_OUT_FORMATS:
        raise ValueError(f'Output format must be one of: {", ".join(ACCEPTED_OUT_FORMATS)}')

    para = {'query': query_string, 'format': out_format}
    res = requests.get(LILA_SPARQL_URL, params=para)
    return res
