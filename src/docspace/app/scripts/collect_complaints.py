from pathlib import Path
import requests
import time
import pandas as pd
from tqdm import tqdm
from transformers import pipeline
import urllib
import os
from django.contrib.auth import get_user_model
from django.core.files import File
from app import *
import docspace

recap_headers = {'Authorization': 'Token ' + docspace.config['COURTLISTENER_TOKEN']}

def search_recap(url, page=1):
    url = "https://www.courtlistener.com/api/rest/v3/search/?" + url.split('?')[-1]
    if page > 1:
        url += '&page=%i' % page
    r = requests.get(url, headers=recap_headers)
    return r.json()


index_path = docspace.config['DATA_DIR'] / 'complaints_index.csv'
complaints_dir = docspace.config['DATA_DIR'] / 'complaints'
complaints_dir.mkdir(exist_ok=True)

if not index_path.exists():
    url = "https://www.courtlistener.com/?q=&type=r&order_by=score%20desc&available_only=on&description=complaint&filed_after=01%2F01%2F2017&filed_before=02%2F01%2F2017"
    num_pages = search_recap(url)['count'] // 20 + 1

    data = []
    for page in tqdm(range(1, num_pages + 1)):
        time.sleep(1)
        r = search_recap(url, page=page)
        data.append(pd.DataFrame(r['results']))
    data = pd.concat(data)
    data.to_csv(index_path, index=False)

index = pd.read_csv(index_path)

if not 'is_complaint' in index.columns:
    model = pipeline("text-classification", model='scales-okn/ontology-complaint', device=0)
    preds = model(index['description'].tolist(), batch_size=16, max_length=256, truncation=True)
    index['is_complaint'] = [x['label'] == 'LABEL_1' for x in preds]
    index.to_csv(index_path, index=False)


index = index[index['is_complaint']].sample(20)
for row in tqdm(index.to_dict('records')):
    filename = row['caseName'].replace('/',' ') + '.pdf'
    doc_path = complaints_dir / filename
    if not doc_path.exists():
        doc_url = "https://storage.courtlistener.com/recap/" + row['filepath_local'].split('recap/')[-1]
        urllib.request.urlretrieve(doc_url, doc_path)
        time.sleep(0.2)


doc_names = [x.name for x in Document.objects.all()]
doc_paths = list(complaints_dir.glob('*.pdf'))
user = get_user_model().objects.get(username='nathan')
for path in tqdm(doc_paths):
    doc_name = path.name
    if doc_name not in doc_names:
        doc = Document(
            name=doc_name,
            upload_by=user,
            public=True,
        )
        doc.save()
        file = File(open(path, 'rb'))
        doc.pdf.save(os.path.basename(file.name), file)
        doc.process(max_chunks=20)

