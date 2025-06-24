import requests
import os
from tqdm import tqdm

def fetch_and_save_url():
    url = input("Enter a URL to fetch: ").strip()
    path = input("Enter the file name (with extension, or leave blank to use '.html'): ").strip()

    # ✅ URL validation
    if not url.startswith(('http://', 'https://')):
        print("❌ Invalid URL. Must start with http:// or https://")
        return

    # ✅ Default file name
    if not path:
        path = "downloaded_file.html"
    elif '.' not in path:
        path += ".html"

    # ✅ Warn if file already exists
    if os.path.exists(path):
        overwrite = input(f"⚠️ The file '{path}' already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("❌ Operation cancelled.")
            return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # ✅ Get content length (for progress bar)
        total = int(response.headers.get('content-length', 0))

        # ✅ Save with progress bar if file is large
        with open(path, 'wb') as file, tqdm(
            total=total,
            unit='B',
            unit_scale=True,
            desc=path,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                bar.update(len(chunk))

        print(f"\n✅ Successfully fetched content from '{url}' and saved to '{path}'")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network or request error: {e}")
    except IOError as e:
        print(f"❌ File write error: {e}")

# Run the function
fetch_and_save_url()
