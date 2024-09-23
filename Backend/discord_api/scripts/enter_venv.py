import os
import subprocess
import sys

def activate_venv():
    # Determine the current operating system
    if os.name == 'nt':  # Windows
        venv_path = '.\\anisync-venv\\Scripts\\activate'
    else:  # Unix/Linux/Mac
        venv_path = 'anisync-venv/bin/activate'

    # Activate the virtual environment
    activate_script = f'source {venv_path}' if os.name != 'nt' else f'{venv_path}'
    command = f'{activate_script} && python your_script.py'

    # Run the command
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    activate_venv()
