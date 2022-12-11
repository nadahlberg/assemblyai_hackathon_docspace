from tqdm import tqdm
import time
from app import *

chunks = Chunk.objects.all()

for chunk in tqdm(chunks):
    try:
        chunk.get_similar_docs()
    except:
        chunk.delete()
        print('error')
        time.sleep(5)
    print(chunk.similar_docs)

