import requests
from bs4 import BeautifulSoup

root = 'https://www.interviewbit.com/data-science-interview-questions/'
endpoint = '/c2480909_2021_china_second_round'
url = root + endpoint
response = requests.get(root)
print(response)

soup = BeautifulSoup(response.content, 'html.parser')
problems = soup.find_all('span')
# print(problems.select('h3'))
print(problems[0].prettify())
