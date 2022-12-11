from tqdm import tqdm
import threading
import time
from app import *

clusters = Cluster.objects.filter(description__isnull=True)

for cluster in tqdm(clusters):
    t = threading.Thread(target=cluster.get_description)
    t.start()
    time.sleep(1)





