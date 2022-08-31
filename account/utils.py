from elasticsearch import Elasticsearch
from django.conf import settings


es_client = Elasticsearch(
    settings.ES_HOST,
    ca_certs=settings.ES_CA_CERTS_PATH,
    basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
)