from setuptools import setup, find_packages
from pathlib import Path


setup(
	name='docspace',
	version='0.1.0',
	package_dir={'': 'src'},
	packages=find_packages('src'),
	install_requires=[
		'configuration-maker',
    ],
	entry_points={
		'console_scripts': [
			'docspace = docspace:cli',
		],
	},
)
