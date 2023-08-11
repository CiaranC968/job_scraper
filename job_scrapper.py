import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json


base_url = 'https://www.jobapplyni.com/'

def get_requests(url, params):
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    containers = soup.find_all('div', class_='container card mb-2')

    return containers
#test
def switch(lang):
    if lang.lower() == "it":
        return "IT"
    elif lang.lower() == "retail":
        return "Retailing, Wholesaling and Purchasing"
    else:
        return ""

if __name__ == "__main__":
    sector = input("Enter from the following sectors (It, Retail): ")
    name = switch(sector)
    
    if name:
        current_page = 1
        
        # Get today's date in yyyy-mm-dd format
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        # Define the file path using an f-string
        desktop_path = os.path.expanduser("~/Desktop/job_listings")
        file_path = os.path.join(desktop_path, f"{name}_job_listings_{today_date}.txt")

        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
            print("Folder does not exist. Creating folder...")
        
        
        with open(file_path, "w") as file:
            while True:
                params = {'sector': name, 'DoSearch': 'true', 'CurrentPage': str(current_page)}
                url = base_url
                containers = get_requests(url, params)
                
                if not containers:
                    print("No job titles found on the current page. Stopping.")
                    break
                
                for container in containers:
                    job_title_element = container.find('h2', class_='card-title')
                    company_info_element = container.find('p', class_='h5')
                    details_container = container.find('div', class_='col-lg-5 col-md-5 bg-light py-2')

                    if job_title_element and company_info_element and details_container:
                        job_title = job_title_element.a.text.strip()
                        company_info = company_info_element.text.strip()

                        # Check if company_info is not "JobStart Scheme" before writing
                        if company_info != "JobStart Scheme":
                            file.write(f"Job Title: {job_title}\n")
                            file.write(f"Company Info: {company_info}\n")

                            details = details_container.find_all('dt', class_='col-6')
                            values = details_container.find_all('dd', class_='col-6')
                            for detail, value in zip(details, values):
                                detail_label = detail.text.strip()
                                detail_value = value.text.strip()
                                file.write(f"{detail_label}: {detail_value}\n")

                            file.write("\n")
                
                # Increment the current page number
                current_page += 1
                
                # Add a delay between requests to avoid overloading the server
                time.sleep(2)
                
        print(f"Job listings saved to {file_path}")
    else:
        print("Invalid sector entered.")