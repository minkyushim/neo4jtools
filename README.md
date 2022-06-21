# Very simple Neo4j HTTP API Client



## Install

`pip install git+https://github.com/minkyushim/neo4jtools.git`

## How to use

```
client=SimpleNeo4jHTTPAPIClient(url='http://localhost:7474', userid='neo4j', passwd='test')
client
```




    {"classname": "SimpleNeo4jHTTPAPIClient", "url": "http://localhost:7474", "neo4j_version": "4.4.3", "neo4j_edition": "community", "db": "neo4j", "auth": true}



## Execute a simple query

```
client.execute_read_query('match (n) return count(n);')
```




    {'results': [{'columns': ['count(n)'],
       'data': [{'row': [85852],
         'meta': [None],
         'graph': {'nodes': [], 'relationships': []}}]}],
     'errors': []}



## Execute a query and return a tabular-type result

```
import pandas as pd
result=client.execute_read_query('match p=(n)-[r]-(m) return n.identifier, n.name, type(r), m.identifier, m.name limit 3;', output_format='row')
pd.DataFrame(result)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>n.identifier</th>
      <th>n.name</th>
      <th>type(r)</th>
      <th>m.identifier</th>
      <th>m.name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GO:0000002</td>
      <td>mitochondrial genome maintenance</td>
      <td>PARTICIPATES_GpBP</td>
      <td>4358</td>
      <td>MPV17</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GO:0000002</td>
      <td>mitochondrial genome maintenance</td>
      <td>PARTICIPATES_GpBP</td>
      <td>291</td>
      <td>SLC25A4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>GO:0000002</td>
      <td>mitochondrial genome maintenance</td>
      <td>PARTICIPATES_GpBP</td>
      <td>55186</td>
      <td>SLC25A36</td>
    </tr>
  </tbody>
</table>
</div>



## Execute a query and return a graph-type result

```
result=client.execute_read_query('match p=()--() return p limit 3;', output_format='graph')
result
```




    {'nodes': [{'identifier': '4358',
       'name': 'MPV17',
       'label': 'Gene',
       'source': 'Entrez Gene:210321',
       'license': 'CCO 1.0',
       'description': 'mitochondrial inner membrane protein MPV17',
       'chromosome': '2',
       'minkyu_degree': 14.0,
       'url': 'http://identifiers.org/ncbigene/4358'},
      {'identifier': 'GO:0000002',
       'name': 'mitochondrial genome maintenance',
       'label': 'BiologicalProcess',
       'source': 'Gene Ontology:2021-02-01',
       'license': 'CC BY 4.0',
       'description': nan,
       'chromosome': nan,
       'minkyu_degree': nan,
       'url': 'http://purl.obolibrary.org/obo/GO:0000002'},
      {'identifier': '291',
       'name': 'SLC25A4',
       'label': 'Gene',
       'source': 'Entrez Gene:210321',
       'license': 'CCO 1.0',
       'description': 'solute carrier family 25 member 4',
       'chromosome': '4',
       'minkyu_degree': 123.0,
       'url': 'http://identifiers.org/ncbigene/291'},
      {'identifier': '55186',
       'name': 'SLC25A36',
       'label': 'Gene',
       'source': 'Entrez Gene:210321',
       'license': 'CCO 1.0',
       'description': 'solute carrier family 25 member 36',
       'chromosome': '3',
       'minkyu_degree': 2.0,
       'url': 'http://identifiers.org/ncbigene/55186'}],
     'edges': [{'type': 'PARTICIPATES_GpBP',
       'start_identifier': '4358',
       'start_name': 'MPV17',
       'end_identifier': 'GO:0000002',
       'end_name': 'mitochondrial genome maintenance',
       'license': 'CC By 4.0',
       'unbiased': 'False',
       'source': 'NCBI gene2go',
       'version': '2021-02-01'},
      {'type': 'PARTICIPATES_GpBP',
       'start_identifier': '291',
       'start_name': 'SLC25A4',
       'end_identifier': 'GO:0000002',
       'end_name': 'mitochondrial genome maintenance',
       'license': 'CC By 4.0',
       'unbiased': 'False',
       'source': 'NCBI gene2go',
       'version': '2021-02-01'},
      {'type': 'PARTICIPATES_GpBP',
       'start_identifier': '55186',
       'start_name': 'SLC25A36',
       'end_identifier': 'GO:0000002',
       'end_name': 'mitochondrial genome maintenance',
       'license': 'CC By 4.0',
       'unbiased': 'False',
       'source': 'NCBI gene2go',
       'version': '2021-02-01'}]}



## Show the graph

```
client.show('match p=()--() return p limit 3;')
```
