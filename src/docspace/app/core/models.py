import tempfile
import os
from pathlib import Path
import pypdfium2 as pdfium
from toolz import partition_all
import pandas as pd
from postgres_copy import CopyManager
import uuid
from tqdm import tqdm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.db import models
import docspace
from .utils import *


class Chunk(models.Model):
    doc = models.ForeignKey('Document', on_delete=models.CASCADE)
    page = models.IntegerField()
    chunk_index = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    clean_text = models.TextField(blank=True, null=True)

    objects = CopyManager()


def pdf_path(instance, filename):
    return f'pdf/{instance.id}.pdf'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    pdf = models.FileField(upload_to=pdf_path, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    clean_text = models.TextField(blank=True, null=True)
    info = models.JSONField(default=dict)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    upload_session = models.CharField(max_length=255, blank=True, null=True)
    last_processed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            input_path = temp_dir / 'doc.file'
            
            with open(input_path, 'wb') as w:
                w.write(self.pdf.file.read())


            pdf = pdfium.PdfDocument(str(input_path))
            return pdf

    def process(self):
        Chunk.objects.filter(doc=self).delete()
        pdf = self.load()

        chunk_size = 64
        chunks = [{'tokens': [], 'page': 0, 'chunk_index': 0}]

        for page_index, page in enumerate(pdf):
            textpage = page.get_textpage()
            for rect in textpage.get_rectboxes():
                text = textpage.get_text_bounded(*rect)
                tokens = text.split()
                if len(tokens) + len(chunks[-1]['tokens']) < chunk_size:
                    chunks[-1]['tokens'] += tokens
                else:
                    chunks.append({
                        'tokens': tokens,
                        'page': page_index,
                        'chunk_index': len(chunks),
                    })

        tokens = []
        for i, chunk in tqdm(list(enumerate(chunks))):
            chunk['doc_id'] = str(self.id)
            if i < len(chunks) - 1:
                chunk['tokens'] += chunks[i + 1]['tokens']
            chunk['text'] = ' '.join(chunk['tokens'])
            chunk['clean_text'] = docspace.utils.clean_text(chunk['text'])
            tokens += chunk['tokens']
            del chunk['tokens']

        chunks = pd.DataFrame(chunks)
        Chunk.objects.from_csv(df_to_file(chunks))
        
        self.text = ' '.join(tokens)
        self.clean_text = docspace.utils.clean_text(self.text)
        self.last_processed = timezone.now()
        self.save()
    
    def chunks(self):
        return Chunk.objects.filter(doc=self).order_by('chunk_index')