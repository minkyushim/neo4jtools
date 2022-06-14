# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['SimpleNeo4jHTTPAPIClient']

# Cell
import os,json,base64
import requests
import pandas as pd
from .dwpc import make_dwpc_query
from .utils import graph_renderer, row_renderer
from .graph import draw

class SimpleNeo4jHTTPAPIClient:

    def __init__(self, url, db='neo4j', userid=None, passwd=None):
        self.url=url
        self.set_serverinfo(url)
        self.setdb(db)
        self.authtoken=None
        if userid is not None:
            self.authtoken=self.get_authtoken(userid, passwd)

    def set_serverinfo(self,url):
        resp=requests.get(url)
        obj=resp.json()
        self.bolt_routing=obj['bolt_routing']
        self.transaction=obj['transaction']
        self.bolt_direct=obj['bolt_direct']
        self.neo4j_version=obj['neo4j_version']
        self.neo4j_edition=obj['neo4j_edition']

    def setdb(self, db):
        self.db=db

    def execute_read_query(self, query, output_format=['row','graph']):
        return execute_query(self, query, output_format)

    def execute_query(self, query, output_format=['row','graph']):
        url=self.transaction.format(databaseName=self.db) + '/commit'
        headers={
            "content-type": "application/json"
        }
        if self.authtoken is not None:
            headers['authorization']="Basic {}".format(self.authtoken)

        if isinstance(output_format, list):
            resultDataContents = output_format
        else:
            resultDataContents = [output_format]

        statement={
          "statements": [
            {
              "statement": query,
              "resultDataContents": resultDataContents
            }
          ]
        }
        resp=requests.post(url,
                           data=json.dumps(statement),
                           headers=headers)

        output= resp.json()

        if len(output['errors']) > 0:
            raise Exception(output['errors'])


        output_renderer=None
        if output_format=='row':
            output_renderer=row_renderer

        if output_format=='graph':
            output_renderer=graph_renderer

        if output_renderer:
            output=output_renderer(output)

        return output

    def show(self, query):
        graph= self.execute_read_query(query, output_format='graph')
        return draw([graph])

    def calculate_dwpc(self, genes, reltype, hops,
                       dwpc_score_prop_name='dwpc_score',
                       only_relations_with_pmid=True,
                       debug=False):
        qry=make_dwpc_query(genes,
                            reltype=reltype,
                            hops=hops,
                            dwpc_score_prop_name=dwpc_score_prop_name,
                            only_relations_with_pmid=only_relations_with_pmid)
        if debug:
            print(qry)

        results=self.execute_read_query(qry, output_format='row')

        return results

    def __repr__(self):
        return json.dumps({
            'classname':self.__class__.__name__,
            'url':self.url,
            'neo4j_version':self.neo4j_version,
            'neo4j_edition':self.neo4j_edition,
            'db':self.db,
            'auth': self.authtoken is not None
        })

    @staticmethod
    def get_authtoken(userid, passwd):
        authstr='{}:{}'.format(userid, passwd)
        b64token=base64.b64encode(authstr.encode())
        strtoken=b64token.decode()
        return strtoken