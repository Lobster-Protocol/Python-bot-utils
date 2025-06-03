# Python-bot-utils
A toolbox to easily setup each bot for the algorithms (converts algo output into calldata)

## Installation

### Install from GitHub
You can install this library directly from GitHub using pip:

```bash
pip install git+https://github.com/Lobster-Protocol/Python-bot-utils.git
```

Or if you want to install a specific branch:
```bash
pip install git+https://github.com/Lobster-Protocol/Python-bot-utils.git@branch-name
```

### Development Installation
For local development and contributing:

```bash
make venv
```
```bash
source .venv/bin/activate
```
```bash
make install
```

## Usage
After installation, you can import the library in your Python code:
```python
import python_bot_utils
# or import specific modules
from python_bot_utils import your_module
```

## Development

Format the code:
```bash
make fmt
```
Ensure formatting is correct:
```bash
make check
```
