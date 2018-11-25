import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import DC, RDFS

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_movies_graph():
    if 'm_graph' not in current_app.config:
        current_app.config['m_graph'] = rdflib.Graph()
        current_app.config['m_graph'].parse('mbook/data/movies.ttl',
                                            format="n3")
    return current_app.config['m_graph']

def get_books_graph():
    if 'b_graph' not in current_app.config:
        current_app.config['b_graph'] = rdflib.Graph()
        current_app.config['b_graph'].parse('mbook/data/book_reviews.ttl',
                                            format="n3")
    return current_app.config['b_graph']

def search(title):
    # Movie query
    m_q = prepareQuery(
          """
          SELECT ?movie
                 ?m_title
                 ?m_year
                 (group_concat(distinct ?m_genre;separator=", ") as ?m_genres)
                 ?m_rating
                 ?b_title
                 ?b_rating
          WHERE {
              ?movie rdfs:label ?m_title .
              ?movie dc:date ?m_year .
              ?movie dc:type ?m_genre .
              ?movie dc:hasRating ?m_rating .
              FILTER(regex(str(?m_title), ?q_title, "i"))
          }
          """,
          initNs={ 'dc': DC,
                   'rdfs': RDFS}
    )
    
    #Book Query
    b_q = prepareQuery(
          """
          SELECT ?book ?b_title ?b_rating
          WHERE {
              ?book dc:hasTittle ?b_title .
              ?book dc:hasRating ?b_rating .
              FILTER(regex(str(?b_title), ?q_title, "i"))
          }
          """,
          initNs={ 'dc': DC,
                   'rdfs': RDFS}
    )
    queryTitle = rdflib.Literal(title)
    mres = get_movies_graph().query(m_q,
                                    initBindings={'q_title': queryTitle})
    #bres = get_books_graph().query(b_q,
    #                               initBindings={'q_title': queryTitle})
    bres = []
    return mres, bres
