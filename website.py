import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time


def download_file(url, output_dir):
    """Download a single file and save it to the output directory."""
    try:
        response = requests.get(url)
        # Extract filename from URL, defaulting to index.html for the main page
        filename = os.path.basename(url)
        if not filename:
            filename = 'index.html'
            
        filepath = os.path.join(output_dir, filename)
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
        return response.text if filename.endswith(('.html', '.htm')) else None
        
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return None


def download_website(url, output_dir):
    """Download a website and all its resources."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the main HTML file
    html_content = download_file(url, output_dir)
    if not html_content:
        return
    
    # Parse HTML to find all resources
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find and download all resources
    for tag in soup.find_all(['img', 'link', 'script']):
        # Get the resource URL
        resource_url = None
        if tag.get('src'):
            resource_url = tag['src']
        elif tag.get('href'):
            resource_url = tag['href']
            
        if resource_url:
            # Convert relative URLs to absolute URLs
            absolute_url = urllib.parse.urljoin(url, resource_url)
            # Add a small delay to avoid overwhelming the server
            time.sleep(0.1)
            download_file(absolute_url, output_dir)


def main():
    url = "https://www.ethan.ws/assets/resume/"
    output_dir = os.path.expanduser("~/Desktop/my_resume")

    try:
        print(f"Starting download of {url} to {output_dir}")
        download_website(url, output_dir)
        print(f"\nWebsite downloaded successfully to {output_dir}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()