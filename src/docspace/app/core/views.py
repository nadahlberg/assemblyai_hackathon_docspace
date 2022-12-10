from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
import pandas as pd
from .models import *
from .utils import *


def index_view(request):
    if request.user.is_authenticated:
        return redirect('core:docs')
    return redirect('core:upload')


def upload_view(request):
    print(request.session._get_or_create_session_key())
    if 'upload_file' in request.FILES:
        doc = dict(
            name=request.FILES['upload_file'].name,
            pdf=request.FILES['upload_file'],
        )
        if request.user.is_authenticated:
            doc['upload_by'] = request.user
        else:
            doc['upload_session'] = request.session._get_or_create_session_key()
        doc = Document(**doc)
        doc.save()
        doc.process()
        return redirect('core:doc', doc_id=doc.id)
    return render(request, 'core/upload.html', {
    })

def about_view(request):
    return redirect('core:index')


def docs_view(request):
    if request.user.username == 'nathan':
        docs = Document.objects.all()
    elif request.user.is_authenticated:
        docs = Document.objects.filter(upload_by=request.user)
    else:
        docs = Document.objects.filter(upload_session=request.session._get_or_create_session_key())

    if 'delete' in request.POST:
        doc = Document.objects.get(id=request.POST['delete'])
        doc.pdf.delete()
        doc.delete()

    if 'rename' in request.POST:
        doc = Document.objects.get(id=request.POST['rename'])
        doc.name = request.POST['new_name']
        doc.save()

    if 'download' in request.POST:
        doc = Document.objects.get(id=request.POST['download'])
        name = doc.name
        if not name.lower().endswith('.pdf'):
            name += '.pdf'
        return download_file(request, doc.pdf.file, name, content_type='application/pdf')
    
    if docs.count() == 0:
        return redirect('core:upload')

    return render(request, 'core/docs.html', {
        'docs': docs,
    })


def doc_view(request, doc_id):
    doc = Document.objects.get(id=doc_id)
    print(doc.upload_session)
    print(request.session._get_or_create_session_key())
    if (doc.upload_by is None or request.user != doc.upload_by) and request.session._get_or_create_session_key() != doc.upload_session:
        return HttpResponseForbidden()
    return render(request, 'core/doc.html', {
        'doc': doc,
    })


def login_view(request):
    if request.POST:
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('core:index')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:index')
