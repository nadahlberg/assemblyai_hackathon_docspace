from tqdm import tqdm
from app import *

clusters = Cluster.objects.filter(description__isnull=True)

for cluster in tqdm(clusters):
    cluster.get_description()
    print('\n\n\n\n')
    print(cluster.description)

