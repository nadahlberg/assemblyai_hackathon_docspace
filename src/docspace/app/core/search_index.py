from django.conf import settings
import numpy as np
import faiss

search_index = faiss.read_index(str(settings.BASE_DIR / 'search_index' / 'index.faiss'))
encodings = np.load(str(settings.BASE_DIR / 'search_index' / 'encodings.npy'))
centroids = np.load(str(settings.BASE_DIR / 'search_index' / 'kmeans_centroids.npy'))
kmeans = faiss.Kmeans(encodings.shape[-1], 200, niter=0, nredo=0, seed=42)
kmeans.train(encodings, init_centroids=centroids)