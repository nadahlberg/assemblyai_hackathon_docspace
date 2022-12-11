import pandas as pd
import numpy as np
import faiss
from tqdm import tqdm
import docspace
from app import *

n_clusters = 100

Cluster.objects.all().update(description=None)
Chunk.objects.all().update(cluster=None)
Chunk.objects.all().update(similar_docs=None)
chunks = Chunk.objects.filter(summary_array__isnull=False, doc__public=True).values()
chunks_ids = [str(x['id']) for x in chunks]
encodings = np.array([x['summary_array'] for x in chunks]).astype(np.float32)

index = docspace.SearchIndex(chunks_ids, encodings)
index.save('search_index')

kmeans = faiss.Kmeans(encodings.shape[-1], n_clusters, niter=50, verbose=True, seed=42)
kmeans.train(encodings)
_, clusters = kmeans.index.search(encodings, 1)
clusters = [x[0] for x in clusters]
for chunks_id, cluster in tqdm(list(zip(chunks_ids, clusters))):
    chunk = Chunk.objects.get(id=int(chunks_id))
    chunk_clusters = Cluster.objects.filter(cluster_id=cluster)
    if not chunk_clusters.exists():
        chunk.cluster = Cluster.objects.create(cluster_id=cluster)
    else:
        chunk.cluster = chunk_clusters.first()
    chunk.save()
