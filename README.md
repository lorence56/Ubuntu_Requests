# Ubuntu Image Fetcher

A small, mindful helper script to download images from the web and save them to a local `Fetched_Images/` folder.

## What this script does

- Prompts the user to enter one or more image URLs (comma-separated).
- Fetches each URL using a respectful User-Agent header.
- Validates the response is an image via the `Content-Type` header.
- Saves the image bytes to `Fetched_Images/` using either the filename from the URL or a generated name.
- Skips duplicate files (doesn't overwrite existing files) and prints a short summary.

## Files

- `image_fetcher.py` — main script (interactive). You can also import `fetch_image` from it to use programmatically.
- `Fetched_Images/` — folder where downloaded images are saved (created automatically on first run).

## Requirements

- Python 3.7+
- The `requests` library

Install the dependency with pip (PowerShell example):

```powershell
python -m pip install --user requests
```

## Usage (interactive)

Run the script from the project root in PowerShell or any shell:

```powershell
python .\image_fetcher.py
```

When prompted, paste one or more image URLs separated by commas, for example:

```
Please enter one or more image URLs (separated by commas): https://example.com/pic.jpg, https://example.com/another.png
```

The script will attempt to download each link and will show status messages like:

- `✓ Successfully fetched: pic.jpg`
- `⚠️ Skipped: The URL does not point to an image. (Type: text/html)`
- `⚠️ Duplicate detected: pic.jpg already exists. Skipping download.`
- `✗ Connection error: ...`

After completion you'll see a summary showing how many images were fetched.

## Programmatic use

You can import and call `fetch_image` from other Python code if you want more control:

```python
from image_fetcher import fetch_image

# Save to the default folder
fetch_image('https://example.com/picture.jpg')

# Save to a custom folder
fetch_image('https://example.com/picture.jpg', folder='my_images')
```

Function contract

- Inputs: `url` (string), optional `folder` (string).
- Output: filename (string) on success, `None` on failure or skip.
- Side-effects: creates `folder` if missing and writes image file.
- Errors: prints user-friendly messages for network errors, non-image content, and unexpected exceptions.

## Implementation notes

- The script sends requests with a `User-Agent: UbuntuFetcher/1.0 (Respectful Client)` header and a 10 second timeout.
- It checks `Content-Type` to ensure the response is an image and avoids saving non-image responses.
- If the URL path contains no filename, a deterministic filename is generated using an 8-character md5 hash of the URL (e.g. `image_a1b2c3d4.jpg`).
- Duplicate prevention: the script checks for an existing file with the same filename and skips download if already present. It does not compare file contents or provide deduplication beyond filename checks.

## Edge cases and behavior

- Non-image URLs — the script will skip and print a warning.
- Slow/unresponsive servers — the request uses a 10s timeout; network errors are caught and reported.
- Filenames containing query parameters — only the path portion of the URL is used to extract a filename.
- Large downloads — the script reads response content into memory before writing; for very large images this may use memory proportional to the file size.

## Troubleshooting

- If you see `Connection error` messages, check your internet connection, firewall, or if the target server blocks automated clients.
- If images are skipped as duplicates but you expect new content, verify the remote filename — the script uses the URL path's basename to name files.
- To see more control (retries, chunked downloads, content hashing), consider modifying `fetch_image` to stream the response and compute hashes.

## Extending the script

- Add CLI args (argparse) to accept an input file of URLs or a single URL argument.
- Stream downloads with `response.iter_content(chunk_size=8192)` for memory-efficient large files.
- Add content hashing (e.g., sha256) to detect true duplicates across different filenames.

## License

This README and the script may be used and adapted freely. No warranty.

---

If you'd like, I can also:
- add argparse-based CLI flags (URL file, output folder, verbose), or
- add a small test that calls `fetch_image` on a mocked requests response.
