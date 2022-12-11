from pathlib import Path
from configuration_maker import Config, ConfigKey
from django.core.management.utils import get_random_secret_key

keys = [
    ConfigKey(
		name='DATA_DIR',
		key_type='path',
	),

	ConfigKey(
		name='COURTLISTENER_TOKEN',
		default=None,
	),

	ConfigKey(
		name='COHERE_API_KEY',
		default=None,
	),

	ConfigKey(
		name='DJANGO_SECRET_KEY',
		default=get_random_secret_key(),
	),

    ConfigKey(
		name='DJANGO_ALLOWED_HOSTS',
		default='localhost,127.0.0.1'
	),

    ConfigKey(
		name='POSTGRES_HOST',
	),

    ConfigKey(
		name='POSTGRES_PORT',
        key_type='int',
	),

	ConfigKey(
		name='POSTGRES_USERNAME',
	),

    ConfigKey(
		name='POSTGRES_PASSWORD',
	),

	ConfigKey(
		name='S3_ACCESS_KEY',
	),

	ConfigKey(
		name='S3_SECRET_KEY',
	),

    ConfigKey(
		name='DEBUG',
        key_type='int',
		default=0,
	),


	ConfigKey(
		name='DEVELOPMENT_MODE',
        key_type='int',
		default=0,
	),
]


config = Config(
	path=Path.home() / '.cache' / 'docspace' / 'config.json',
	config_keys=keys,
	cli_command='docspace configure',
)
