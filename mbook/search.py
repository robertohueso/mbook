import functools
import mbook.rdf as rdf

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET', 'POST'))
def search():
    return render_template('search.html')

@bp.route('/results', methods=('GET', 'POST'))
def results():
    if request.args.get('searchQuery', None):
        context = {}
        context['movie'] = []
        context['book'] = []
        query = str(request.args['searchQuery'])
        context['query'] = query
        mres, bres = rdf.search(query)
        for row in mres:
            new_mov = {}
            new_mov['m_title'] = row['m_title']
            new_mov['m_year'] = row['m_year']
            new_mov['m_genre'] = row['m_genre']
            new_mov['m_rating'] = row['m_rating']
            context['movie'].append(new_mov)
        for row in bres:
            new_book = {}
            new_book['b_title'] = row['b_title']
            new_book['b_rating'] = row['b_rating']
            context['book'].append(new_book)
        return render_template('results.html', cont=context)
    else:
        return redirect(url_for('search.search'))
