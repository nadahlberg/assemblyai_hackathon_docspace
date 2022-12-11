from tqdm import tqdm
from app import *

chunks = Chunk.objects.all()

for chunk in tqdm(chunks):
    chunk.get_similar_docs()
    print(chunk.similar_docs)

