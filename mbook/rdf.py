import rdflib
from rdflib.plugins.sparql import prepareQuery

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_graph():
    if 'graph' not in g:
        g.graph = rdflib.Graph()
        g.graph.parse('mbook/data/movies.ttl', format="n3")
    return g.graph

def search(title):
    q = prepareQuery(
        """
        SELECT ?movie ?m_title ?m_year ?m_genre ?b_title ?b_author
        WHERE {
            ?movie rdfs:label ?m_title .
        }
        """)
    queryTitle = rdflib.Literal(title)
    qres = get_graph().query(q, initBindings={'m_title': queryTitle,
                                              'b_title': queryTitle})
    return qres
