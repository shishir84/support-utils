from elasticsearch import Elasticsearch
from core import settings

_es = None


def get_es():
    global _es
    if _es is None:
        _es = Elasticsearch(settings.ES_ENDPOINT)
    return _es


def search_index(index: str, body: dict):
    es = get_es()
    return es.search(index=index, body=body)
