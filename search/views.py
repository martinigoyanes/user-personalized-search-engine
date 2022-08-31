import json
import urllib3
from turtle import right
from django.shortcuts import redirect, render
from search.utils import es_client
from django.conf import settings
from elasticsearch import ConnectionError, AuthenticationException
from django.contrib.auth.models import User
from datetime import datetime



def index(request):
    return render(request, 'index.html')


def health(request):
    info = None
    info_str = None
    error_msg = None

    try:
        info = es_client.info()
        info_str = json.dumps(info.body, indent=4)
    except ConnectionError:
        error_msg = 'Cannot connect to elasticsearch on {}'.format(
            settings.ES_HOST
        )
    except AuthenticationException:
        error_msg = 'Wrong username or password'
    except Exception as e:
        error_msg = str(e)

    return render(request, 'health.html', {
        'info': info,
        'info_str': info_str,
        'error_msg': error_msg
    })


def search(request):
    query = request.GET.get('query')   # Get query from POST data
    page = request.GET.get('page', 1)   # Get page from POST data, default to 1
    page_size = 10   # Default page size

    try:
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    # If query is empty, redirect to home page
    if query is None or len(query) == 0:
        return redirect('index')

    # Log the query to the user profile
    query_doc = {'username': request.user.username, 'search': query, 'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')}
    es_client.index(index='queries', body=query_doc)

    # Perform phrase search
    resp = es_client.search(index='enwikiquote', from_=(page - 1) * page_size, size=page_size, query={
        'match_phrase': {
            'text': query
        }
    })

    # Select fields from results
    results = map(lambda x: {
        'id': x['_id'],
        'title': x['_source']['title'],
        'summary': x['_source']['text'][:300],
        'category': x['_source']['category'],
        'score': x['_score'],
    }, resp['hits']['hits'])

    count = resp['hits']['total']['value']
    previous = '?query={0}&page={1}'.format(
        query, page - 1) if page > 1 else None
    next = '?query={0}&page={1}'.format(
        query, page + 1) if page * page_size < count else None
    left_bound = max(page - 5, 1)
    right_bound = min(left_bound - 1 + 10, count // page_size + 1)
    pagination = map(lambda x: {
        'page': x,
        'url': '?query={0}&page={1}'.format(query, x)
    }, range(left_bound, right_bound + 1))

    return render(request, 'result.html', {
        # Time spent
        'time': resp['took'] / 1000,    # milliseconds to seconds
        # Data
        'count': count,
        'results': results,
        # Pagination
        'current': page,
        'previous': previous,
        'next': next,
        'pagination': pagination
    })
