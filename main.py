import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def check_domain(url, link):
    """
    function to check if link is internal or external
    """
    parsed_uri = urlparse(url)
    domain = parsed_uri.netloc
    parsed_link = urlparse(link)
    link_domain = parsed_link.netloc
    if domain == link_domain:
        return True
    else:
        return False


def convert_relative_to_absolute(url, link):
    """
    function to convert relative link to absolute
    """
    if not link.startswith("http"):
        link = urljoin(url, link)
    return link


def extract_all_links(url):
    """
    function to extract all the links from a webpage
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        href = convert_relative_to_absolute(url, href)
       # print(href)
        links.add(href)
    return links


# Function to extract all links from a webpage
def extract_links(url):
    # Create sets for internal and external links
    internal_links = set()
    external_links = set()
    visited_links = set()

    # Use a queue to store URLs to visit
    queue = [url]

    # While there are URLs to visit
    while queue:
        # Dequeue the next URL
        current_url = queue.pop(0)
        visited_links.add(current_url)

        # Extract all links
        links = extract_all_links(current_url)

        for link in links:
            if check_domain(url, link):
                if link not in visited_links:
                    internal_links.add(link)

                    if link not in queue:
                        # add internal links to queue
                        print(link)
                        queue.append(link)
            else:
                external_links.add(link)

    # Return the sets of links
    return internal_links, external_links


# Example usage
internal, external = extract_links("https://gotonews.com")
print('Internal links:', internal)
print('External links:', external)
