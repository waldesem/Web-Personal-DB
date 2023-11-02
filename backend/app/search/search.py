from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = False,
    verify_serts = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = 'persons_index'


def add_to_index(model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    if model.__tablename__ == 'persons':
        client(index=index_name, doc_type=index_name, 
               id=model.id, body=payload)
    else:
        client(index=index_name, doc_type=index_name, 
               id=model.person_id, body=payload)

def remove_from_index(model):
    client.delete(index=index_name, 
                  doc_type=index_name, id=model.id)

def query_index(query):
    search = client.search(
        index=index_name, doc_type=index_name,
        body={
            'query': {
                'multi_match': {
                    'query': query, 'fields': ['*']
                    }
                }
            }
        )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids