import requests
from bs4 import BeautifulSoup
import csv

keyword = 'hotels'
location = 'London'
url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=951826076&keywords={}&location={}&pageNum='.format(keyword, location)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
data = []

for page in range(1, 11):
    req = requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'row businessCapsule--mainRow')
    for i in items:
        name = i.find('span', 'businessCapsule--name').text
        address = ''.join(i.find('span', {'itemprop': 'address'}).text.strip().split('\n'))
        try:
            web = i.find('a', {'rel': 'nofollow noopener'})['href'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        except:
            web = ''
        try:
            phone = i.find('span', 'business--telephoneNumber').text
        except:
            phone = ''
        image = i.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'htt' not in image:
            image = ''
        data.append([name, address, web, phone, image])

write = csv.writer(open('result/{}_{}.csv'.format(keyword, location), 'w', newline=''))

write.writerow(['Name', 'Address', 'Website', 'Phone Number', 'Image URL'])
for d in data:
    write.writerow(d)
