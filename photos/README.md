# Original photographs only

The import tool copies photo media into this directory from your own Instagram JSON export or CSV-curated images.

Only commit images you want to publish publicly. The original ZIP export and the local SQLite database should stay private.

Import runs may leave older unused images behind; remove unused images manually before publishing if needed.

Supported on the web: JPG, PNG, WebP. For improved EXIF privacy, first run `python3 -m pip install Pillow` so imported images are normalized and their EXIF metadata stripped. Otherwise the standard library fallback copies image metadata unchanged.
