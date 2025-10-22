import requests

def web_scraping():
    URLs = {
        "BigBang_VersionNumbers": "https://random/images.txt",
    }
    lines = []

    containers = {}

    for key in URLs:
        page = requests.get(URLs[key])
        if page.status_code == 200:
            content=page.text
    
            lines=content.splitlines()

            containers[key] = []

            for line in lines:
                parts = line.split('ironbank/', 1)  # Split into two parts, taking the second part
                if len(parts) > 1:
                    containers[key].append(parts[1])
        
        else:
            print(f"Failed to retrieve content from {URLs}. Status code: {page.status_code}")

    return containers


    