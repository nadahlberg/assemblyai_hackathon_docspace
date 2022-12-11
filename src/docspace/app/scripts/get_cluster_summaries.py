from tqdm import tqdm
from app import *

Cluster.objects.all().update(description=None)

clusters = Cluster.objects.all()

for cluster in tqdm(clusters):
    cluster.get_description()
    print('\n\n\n\n')
    print(cluster.description)

