import requests
import login
import json
import scrape
import csv


# Convert Selenium cookies to requests cookies
def convert_cookies(cookies):
    requests_cookies = {}
    for cookie in cookies:
        requests_cookies[cookie['name']] = cookie['value']
    return requests_cookies

# Perform API request with the extracted cookies
def make_api_request(cookies, name, tag):
    
    url = f'https://randomVat/api/image?name={requests.utils.quote(name)}&tag={requests.utils.quote(tag)}&branch=master'
    
    response = requests.get(
        url,
        headers={'Accept': 'application/json'},
        cookies=cookies
    )
    
    if response.status_code == 200:
        data = response.json()        
        # Write JSON response to a file
        with open('response.json', 'w') as file:
            json.dump(data, file, indent=4)

        ora_value = data['image']['state']['ora']
        return float(ora_value)
    elif response.status_code == 400:
        print("Bad Request, missing either parameter")
        return -1
    elif response.status_code == 404:
        print("Image not found: ", name, tag)
        return -1

def separate_name_and_tag(full_string):
    try:
        # Split the string by the colon
        name, tag = full_string.split(':', 1)
        return name, tag
    except ValueError:
        # Handle cases where the string does not contain a colon
        print("Error")
        return None, None
    

cookies = login.login()
requests_cookies = convert_cookies(cookies)

# scrape the names of the containers of the big bang instances
containers = scrape.web_scraping()
    
for key in containers:
    print(key)

container_averages = {}


for key in containers:
        averages = 0
        length_of_container = 0

        for i in containers[key]:
            name, tag = separate_name_and_tag(i)
            value = make_api_request(requests_cookies, name, tag)
            if value == -1:
                continue
            else:
                length_of_container += 1
                averages += value
        
        #averages /= len(containers[key])
        print(averages)
        print(length_of_container)
        averages /= length_of_container
        print(key, averages)
        container_averages[key] = averages

field_names = ['Version', 'Average']
with open('averages.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
        
    # Write each entry from container_averages as a row in the CSV file
    for key, value in container_averages.items():
        writer.writerow({'Version': key, 'Average': value})


