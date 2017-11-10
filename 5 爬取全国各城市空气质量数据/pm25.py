"""
	author: dreamkong
	date: 2017/11/09
"""

# 爬取全国各城市空气质量信息

import requests
from bs4 import BeautifulSoup
import csv


def get_city_list():
	url = 'http://pm25.in/'
	url_text = get_html_text(url)
	soup = BeautifulSoup(url_text,'lxml')
	
	city_div = soup.findAll('div',{'class':'bottom'})[1]
	city_link_list = city_div.findAll('a')
	city_list = []
	for city_link in city_link_list:
		city_name = city_link.text
		city_url = city_link['href']
		city_list.append((city_name, city_url))

	return city_list


def get_city_aqi(city_url):
	url = 'http://pm25.in' + city_url
	url_text = get_html_text(url)
	soup = BeautifulSoup(url_text,'lxml')
	div_list = soup.findAll('div',{'class':'span1'})

	city_aqi = []
	for i in range(8):
		div_content = div_list[i]
		# caption = div_content.find('div',{'class':'caption'}).text.strip()
		value = div_content.find('div',{'class':'value'}).text.strip()

		# city_aqi.append((caption, value))
		city_aqi.append(value)

	return city_aqi

def main():
	city_list = get_city_list()
	# for city in city_list:
	# 	city_name = city[0]
	# 	city_url = city[1]
	# 	city_aqi = get_city_aqi(city_url)
	# 	print(city_name, city_aqi)
	header = ['AQI','PM2.5/1h','PM10/1h','CO/1h','NO2/1h','O3/1h', 'O3/8h','SO2/1h']

	with open('china_city_aqi.csv', 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		for i, city in enumerate(city_list):
			if (i + 1) % 10 == 0:
				print('已爬取{}条,共{}条记录'.format(i + 1, len(city_list)))

			city_name = city[0]
			city_url = city[1]
			city_aqi = get_city_aqi(city_url)
			row = [city_name] + city_aqi
			writer.writerow(row)


if __name__ == '__main__':
	main()

