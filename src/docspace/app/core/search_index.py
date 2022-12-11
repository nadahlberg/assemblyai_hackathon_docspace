from django.conf import settings
import numpy as np
import docspace
import faiss

search_index = docspace.SearchIndex.load(str(settings.BASE_DIR / 'search_index'))
