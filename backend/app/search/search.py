from opensearchpy import OpenSearch


host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    http_compress = True,
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = 'persons_index'

index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

client.indices.create(index_name, body=index_body)


def add_to_index(model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    if model.__tablename__ == 'persons':
        client.index(index=index_name, id=model.id, body=payload)
    else:
        client.index(index=index_name, id=model.person_id, body=payload)

def remove_from_index(model):
    client.delete(index=index_name, id=model.id)

def query_index(query):
    search = client.search(index=index_name, body={'query': {
            'multi_match': {
                'query': query, 'fields': ['*']
                }
            }
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids