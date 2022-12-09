from pathlib import Path
from configuration_maker import Config, ConfigKey


keys = [
    ConfigKey(
		name='DATA_DIR',
		key_type='path',
	),
]


config = Config(
	path=Path.home() / '.cache' / 'docspace' / 'config.json',
	config_keys=keys,
	cli_command='docspace configure',
)
