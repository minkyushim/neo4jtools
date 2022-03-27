# AUTOGENERATED! DO NOT EDIT! File to edit: 02_utils.ipynb (unless otherwise specified).

__all__ = ['parse_result_row_graph', 'drop_duplicates', 'parse_result_graph', 'graph_renderer', 'row_renderer',
           'get_graph_for_ipycytoscape', 'draw']

# Cell
import json
import pandas as pd
import ipycytoscape
from collections import OrderedDict

def parse_result_row_graph(jsonobj):
    '''
    Parse Neo4j HTTP API Graph Result row

    input: element of result list
    output: tuple of nodes and edges
    '''
    def parse_nodes(gobj):
        node_dict={}
        for n in gobj['nodes']:
            _id=n['id']
            label=n['labels'][0]
            props=n['properties']
            props['label']=label

            keys=props.keys()
            headcols=['identifier','name','label']
            orderedkeys=headcols+list(set(keys)-set(headcols))
            orderedobj={k: props[k] for k in orderedkeys}

            node_dict[_id]=orderedobj

        return node_dict

    def parse_edges(gobj, node_dict):
        edges=[]
        for r in gobj['relationships']:
            _type=r['type']
            start_id=r['startNode']
            end_id=r['endNode']

            start_node=node_dict[start_id]
            end_node=node_dict[end_id]

            edge_dict={
                'type': _type,
                'start_identifier':start_node['identifier'],
                'start_name': start_node['name'],
                'end_identifier':end_node['identifier'],
                'end_name': end_node['name']
            }

            # inject the rest properties
            propobj=r['properties']
            for k in propobj:
                edge_dict[k]=propobj[k]

            edges.append(edge_dict)

        return edges

    gobj=jsonobj['graph']

    node_dict=parse_nodes(gobj)
    nodes=[node_dict[k] for k in node_dict]

    edges=parse_edges(gobj, node_dict)

    return nodes, edges

def drop_duplicates(items):
    df=pd.DataFrame(items)
    df=df.drop_duplicates()
    items=df.to_dict(orient='records')

    return items

def parse_result_graph(data):
    '''
    Parse Neo4j HTTP API Graph Result
    '''
    nodes=[]
    edges=[]
    for item in data:
        _nodes, _edges = parse_result_row_graph(item)
        nodes=nodes+_nodes
        edges=edges+_edges

    nodes=drop_duplicates(nodes)
    edges=drop_duplicates(edges)

    return nodes, edges

def graph_renderer(neo4j_output):
    output=neo4j_output['results'][0]
    nodes, edges = parse_result_graph(output['data'])
    output = {'nodes':nodes, 'edges':edges}

    return output

def row_renderer(neo4j_output):
    output=neo4j_output['results'][0]
    cols=output['columns']
    df=pd.DataFrame([e['row'] for e in output['data']], columns=cols)
    output=df.to_dict(orient='records')

    return output

def get_graph_for_ipycytoscape(neo4j_graph_dict):
    g={}
    g['nodes']=[{'data': {
        'id':n['identifier'],
        'name':n['name']
    }} for n in neo4j_graph_dict['nodes']]

    g['edges']=[{'data': {
        'source':e['start_identifier'],
        'target':e['end_identifier']
    }} for e in neo4j_graph_dict['edges']]

    return g

def draw(graphs):
    style = [
        {
            'selector': 'node',
            'style': {
                'label': 'data(name)',
                'background-color': 'rgb(241, 102, 103)'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'target-arrow-shape': 'triangle',
                'font-size': '8px',
                'curve-style': 'bezier',
                'label': 'data(dwpc)',
            }
        },
    ]
    widget = ipycytoscape.CytoscapeWidget()
    gs=[get_graph_for_ipycytoscape(g) for g in graphs]
    for g in gs:
        widget.graph.add_graph_from_json(g, directed=True)
    widget.set_style(style)

    return widget