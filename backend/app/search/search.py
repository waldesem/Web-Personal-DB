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
