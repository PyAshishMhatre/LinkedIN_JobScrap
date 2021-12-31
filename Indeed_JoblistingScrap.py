import requests
from bs4 import BeautifulSoup
import pandas as pd

Search_title = ('%20'.join(input('Enter Job Title').split())).strip()


def Get(page, Search_title = 'data%20analyst'):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    html = f'https://www.indeed.com/jobs?q={Search_title}&l=United%20States&explvl=entry_level&start={page}'

    r=requests.get(html, headers)

    search=BeautifulSoup(r.content,'html.parser')
    return(search)
    
def Extract(soup):
    jobs = soup.find_all('div', class_ ="job_seen_beacon")
    for job in jobs:
        job_title = job.find('h2').text.strip()
        company_name =  job.find('span', class_ = 'companyName').text.strip()
        try:
            company_link = (job.find('span', class_ = 'companyName').find('a', class_="turnstileLink companyOverviewLink"))["href"].strip()
            company_link = 'https://www.indeed.com' + company_link
        except:
            company_link = ''
        company_loc = job.find('div', class_='companyLocation').text.strip()
        try:
            summary = job.find('li').text
        except:
            summary = ''
        try:
            job_comp = job.find('div', class_='attribute_snippet').text.strip()
        except:
            job_comp = ''
        Company_Dict = {
            'Job_Title' : job_title,
            'Company_Name' : company_name,
            'Company_Link' : company_link,
            'Company_location' : company_loc,
            'Company_summary' : summary,
            'Salary' : job_comp }
        data.append(Company_Dict)
    return(data)
data = []
for i in range(0,70,10):
    soup = Get(i, Search_title)
    Extract(soup)
Joblisting = pd.DataFrame(data)
file_name = input('Enter File name')
Joblisting.to_csv(f'{file_name}.csv')