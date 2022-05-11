# jsimager

This tool can be used to create valid images, that can be embedded into `<script src="/path/to/file"></script>` tags. The images can be used to bypass CSP on sites that allow image upload and allow `'self'` as `script-src` directive, but does not allow `inline` or remote scripts.

## Usage

Clone the repositroy, install the requirements and run the scipt.

```
git clone https://github.com/petergyorgy/jsimager.git
cd jsimager
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python jsimager.py --help
```

