from pathlib import Path
import faiss
import numpy as np
import pandas as pd
from toolz import partition_all
from tqdm import tqdm


class SearchIndex():
    def __init__(self, texts, encodings, add_encodings = True):
        self.texts = []
        self.index = faiss.IndexFlatL2(encodings.shape[-1])
        if add_encodings:
            self.texts = texts
            self.index.add(encodings.astype('float32'))
    
    def add(self, texts, encodings):
        self.texts += texts
        self.index.add(encodings.astype('float32'))

    def search(self, query, k):
        index = self.index
        query = query.astype('float32')
        distances, indices = index.search(query, k=k)
        results: list[list[dict]] = []
        for i in range(len(query)):
            results.append([])
            for j in range(k):
                results[-1].append({
                    'text': self.texts[indices[i][j]],
                    'index': indices[i][j],
                    'distance': distances[i][j],
                })
        return results

    def save(self, output_dir):
        index = self.index
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        faiss.write_index(index, str(output_dir / 'index.faiss'))
        pd.DataFrame(self.texts, columns=['texts']).to_csv(output_dir / 'texts.csv', index=False)

    @staticmethod
    def load(input_dir):
        input_dir = Path(input_dir)
        index = faiss.read_index(str(input_dir / 'index.faiss'))
        search_index = SearchIndex([], encodings=np.zeros((0, index.d)), add_encodings=False)
        texts = pd.read_csv(input_dir / 'texts.csv')['texts'].tolist()
        search_index.texts = texts
        search_index.index = index
        return search_index

    def __getitem__(self, item):
        index = self.index
        if isinstance(item, int):
            item = int(item)
            if item < 0:
                item = len(self) + item
            return index.reconstruct(item).astype('float32')
        elif isinstance(item, slice):
            return np.vstack([self[i] for i in list(range(len(self))[item])]).astype('float32')
        elif isinstance(item, list):
            return np.vstack([self[i] for i in item]).astype('float32')
        else:
            return index.reconstruct(int(item)).astype('float32')

    def __len__(self):
        return len(self.texts)