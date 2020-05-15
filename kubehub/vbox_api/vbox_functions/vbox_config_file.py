import re
from pathlib import Path


def config_file(image):
    config_file_path = Path.home() / '.config/VirtualBox/VirtualBox.xml'
    location = image
    location = location.replace("'", "")
    location = re.escape(location)
    pattern = f'<HardDisk.*location=\"{location}\".*/>'
    text = config_file_path.read_text()
    replaced_data = re.sub(pattern, '', text)
    config_file_path.write_text(replaced_data)
    return f'disk {pattern} excluded'
