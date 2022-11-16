# searchable-pdf
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

Utility for converting a pdf file into a searchable pdf (using OCR tesseract).

### Installation

Firstly install [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html).

Then execute the commands below:

```bash
git clone https://github.com/kovalenkong/searchable-pdf.git
cd searchable-pdf/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

```bash
python main.py input.pdf output.pdf
```

where `input.pdf` - source file name and `output.pdf` - output file name.

You can also specify languages or set another value for the maximum number of processes.
Show help on command line and config file options:

```bash
python main.py --help
```
