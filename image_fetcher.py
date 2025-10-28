import requests
import os
import hashlib
from urllib.parse import urlparse

def fetch_image(url, folder="Fetched_Images"):
    """
    Fetches an image from a given URL and saves it in the specified folder.
    Returns the filename if successful, or None if failed.
    """

    try:
        # Create the directory if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Send HTTP request
        headers = {"User-Agent": "UbuntuFetcher/1.0 (Respectful Client)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        # Validate content type before saving
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"⚠️ Skipped: The URL does not point to an image. (Type: {content_type})")
            return None

        # Extract filename or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate a unique name using hash of URL
            filename = f"image_{hashlib.md5(url.encode()).hexdigest()[:8]}.jpg"

        filepath = os.path.join(folder, filename)

        # Prevent duplicate downloads
        if os.path.exists(filepath):
            print(f"⚠️ Duplicate detected: {filename} already exists. Skipping download.")
            return None

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    return None


def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask user for one or multiple URLs
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")

    # Trim whitespace from each URL
    urls = [url.strip() for url in urls if url.strip()]

    if not urls:
        print("⚠️ No URLs provided. Please try again.")
        return

    successful = 0
    for url in urls:
        print(f"\nFetching → {url}")
        if fetch_image(url):
            successful += 1

    print("\n📦 Summary:")
    print(f"Images successfully fetched: {successful}/{len(urls)}")
    print("Connection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
