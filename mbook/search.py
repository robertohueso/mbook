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
        query = str(request.args['searchQuery'])
        context['query'] = query
        qres = rdf.search(query)
        for row in qres:
            context['m_title'] = row['m_title']
            context['m_year'] = row['m_year']
            context['m_genre'] = row['m_genre']
            context['b_title'] = row['b_title']
            context['b_author'] = row['b_author']
        return render_template('results.html', cont=context)
    else:
        return redirect(url_for('search.search'))
