import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def download_images(url, download_folder="downloaded_images"):
    """
    Downloads all images from a given URL to a specified folder.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Created download folder: {download_folder}")

    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src') # type: ignore
        if img_src:
            img_url = urljoin(url, img_src)  # type: ignore # Convert relative URLs to absolute URLs

            try:
                img_response = requests.get(img_url, stream=True)
                img_response.raise_for_status()

                # Extract filename from the URL or assign a default name
                filename = os.path.basename(img_url)
                if not filename:
                    filename = f"image_{hash(img_url)}.jpg"  # Unique filename if none found
                
                filepath = os.path.join(download_folder, filename)

                with open(filepath, 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading image {img_url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while downloading {img_url}: {e}")

# Example usage
target_url = "https://example.com"  # Replace with the URL you want to scrape
download_images(target_url) 
