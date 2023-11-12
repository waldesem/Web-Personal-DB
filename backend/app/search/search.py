from opensearchpy import OpenSearch


host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    http_compress = True,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

class Searching:

    def __init__(self):

        self.index_name = 'persons_index'
        self.index_body = {
        'settings': {
            'index': {
            'number_of_shards': 4
            }
        }
        }
        if not client.indices.exists(self.index_name):
            client.indices.create(self.index_name, body=self.index_body)

    def add_to_index(self, model):
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        if model.__tablename__ == 'persons':
            client.index(index=self.index_name, id=model.id, body=payload)
        else:
            client.index(index=self.index_name, id=model.person_id, body=payload)

    def remove_from_index(self, model):
        client.delete(index=self.index_name, id=model.id)

    def query_index(self, query):
        search = client.search(index=self.index_name, body={'query': {
                'multi_match': {
                    'query': query, 'fields': ['*']
                    }
                }
            }
        )
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids