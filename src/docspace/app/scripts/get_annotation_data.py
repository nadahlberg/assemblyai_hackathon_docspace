import pandas as pd
import json
import docspace
from app import *

chunks = pd.DataFrame(Chunk.objects.values('id', 'text', 'doc_id', 'chunk_index'))
chunks = chunks.sort_values(['doc_id', 'chunk_index'])
chunks = chunks[chunks['text'].notnull()]

data = []
terms = ['CLAIM', 'COUNT', 'CAUSE']
for row in tqdm(chunks.to_dict('records')):
    if any(term in row['text'] for term in terms):
        data.append(row)
    elif any(term in row['text'].lower() for term in ['civ', 'u.s.c.']) and 'violat' in row['text'].lower():
        data.append(row)

data = [{'data': {'text': x['text']}} for x in data]
with open(docspace.config['DATA_DIR'] / 'anno_data.json', 'w') as w:
    w.write(json.dumps(data))
