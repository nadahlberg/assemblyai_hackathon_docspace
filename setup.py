from setuptools import setup, find_packages
from pathlib import Path


setup(
	name='docspace',
	version='0.1.0',
	package_dir={'': 'src'},
	packages=find_packages('src'),
	install_requires=[
		'configuration-maker',
		'Django',
		'django-storages',
		'django-postgres-copy',
		'pandas',
		'pathlib',
		'pikepdf',
		'tqdm',
		'toolz',
		'scikit-learn',
		'nltk',
		'click',
		'gunicorn',
		'pypdfium2',
		'psycopg2-binary', 
		'dj-database-url',
		'whitenoise',
		'plotly',
		'requests',
		'faiss-cpu',
		'protobuf==3.19.6',
		'pypdfium2',
		'boto3',
    ],
	entry_points={
		'console_scripts': [
			'docspace = docspace:cli',
		],
	},
	include_package_data=True,
	package_data={
		'docspace': [str(x) for x in (Path(__file__).parent / 'src/docspace/app/templates').rglob('*')],
	},
)
