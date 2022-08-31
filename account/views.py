from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from account.utils import es_client
import urllib3
import json
import uuid

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            

            # Create user in database
            user_doc = {'username': username, 'password': raw_password}
            es_client.index(index='users', body=user_doc)
            login(request, user)

            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user(request):
    # Search queries for username in ES and retrieve them ordered from newest to oldest
    query = { "bool": { "must": [{"term":{"username": request.user.username}}]}}
    results = es_client.search(index='queries', query=query, sort='timestamp:desc') 

    queries = []
    for r in results['hits']['hits']:
        r = r['_source']
        print(r)
        queries += [{'search': r['search'], 'timestamp': r['timestamp']}]

    return render(request, 'userhistory.html', {'queries': queries})
