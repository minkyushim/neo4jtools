# Very simple Neo4j HTTP API Client



## Install

`pip install git+git://github.com/minkyushim/neo4jtools.git`

## How to use

```python
client=SimpleNeo4jHTTPAPIClient(url='http://localhost:7474', userid='neo4j', passwd='test')
client
```




    {"classname": "SimpleNeo4jHTTPAPIClient", "url": "http://localhost:7474", "neo4j_version": "4.4.3", "neo4j_edition": "community", "db": "neo4j", "auth": true}



```python
client.execute_read_query('match (n) return count(n);')
```




    {'results': [{'columns': ['count(n)'],
       'data': [{'row': [85041],
         'meta': [None],
         'graph': {'nodes': [], 'relationships': []}}]}],
     'errors': []}


