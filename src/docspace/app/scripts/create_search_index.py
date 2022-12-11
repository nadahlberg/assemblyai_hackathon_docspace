import pandas as pd
import numpy as np
import faiss
import docspace
from app import *

chunks = Chunk.objects.filter(summary_array__isnull=False).values()
chunks_ids = [str(x['id']) for x in chunks]
encodings = np.array([x['summary_array'] for x in chunks]).astype(np.float32)

index = docspace.SearchIndex(chunks_ids, encodings)
index.save('search_index')

kmeans = faiss.Kmeans(encodings.shape[-1], 200, niter=20, verbose=True, seed=42)
kmeans.train(encodings)
with open("search_index/encodings.npy", 'wb') as f:
    np.save(f, encodings)
with open("search_index/kmeans_centroids.npy", 'wb') as f:
    np.save(f, kmeans.centroids)

_, clusters = kmeans.index.search(encodings, 1)
clusters = [x[0] for x in clusters]
print(clusters)

chunk = Chunk.objects.get(id=chunks_ids[90])
print(clusters[90])
print(chunk.search())
