import datetime

import requests, json
from fake_useragent import UserAgent
from lxml import etree


class GetHotel:

    def __init__(self):
        self.url = "https://www.bthhotels.com/listasync/"
        self.header = {
            'user-agent': UserAgent().Chrome
        }

    def requests_hotel_phone_API(self, hotel_href):
        response = requests.get(hotel_href, headers=self.header)
        response.encoding = 'utf-8'

        html = etree.HTML(response.text)
        try:
            hotel_phone = html.xpath('/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/p/text()')[0]
        except:
            hotel_phone = '无'
        return hotel_phone

    def requests_room_info(self, hotel_info, beginDate, endDate):

        pass

    def requests_hotel_API(self, cityCode, cityId, pageNo):
        today = datetime.datetime.now()
        beginDate = today.strftime('%Y/%m/%d')
        endDate = (today + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        data = {
            "cityCode": cityId,
            "SelectArea": "",
            "SignleAreaFilter": "",
            "priceRage": "",
            "feature": "",
            "cityName": cityCode,
            "beginDate": beginDate,
            "endDate": endDate,
            "orderBy": "0",
            "pageNo": pageNo,
            "device": "",
            "key": "F",
            "keyDescript": "",
            "Brands": "",
            "SeoParams": "p1"
        }
        response = requests.get(self.url + cityCode, headers=self.header, params=data)
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        hotel_list = html.xpath('//div[@class="list_boxline"]')
        # 酒店id，酒店名称，地址，电话，经度，纬度，图片地址，星级
        for hotel in hotel_list:
            hotel_href = hotel.xpath('.//div[@class="list_intro_name_tj"]/a')[0]
            hotel_id = hotel_href.xpath('./@data-hotelcd')[0]
            hotel_name = hotel_href.xpath('./@title')[0]
            hotel_address = hotel.xpath('.//ul[@class="list_intro_address_tj"]/span/@title')[0]
            hotel_longitude_dimension = hotel.xpath('./@data-point')[0].split(',')
            hotel_longitude = hotel_longitude_dimension[0]
            hotel_dimension = hotel_longitude_dimension[1]
            hotel_image = hotel.xpath('.//div[@class="list_intro_img"]/a/img/@src')[0]
            try:
                hotel_grade = hotel.xpath('.//ul[@class="list_intro_comment_tj star_gaoxing"]/a/code/span/text()')[0]
            except:
                hotel_grade = hotel.xpath('.//div[@class="hotel_star_icon"]/img/@src')[0]
                if 'five' in hotel_grade:
                    hotel_grade = "5.0"
            hotel_phone = self.requests_hotel_phone_API('https://www.bthhotels.com' + hotel_href.xpath('./@href')[0])
            print(hotel_href.xpath('./@href'))
            print(hotel_id)
            print(hotel_name)
            print(hotel_address)
            print(hotel_longitude)
            print(hotel_dimension)
            print(hotel_image)
            print(hotel_grade.strip())
            print(hotel_phone)
            hotel_info = {
                "hotel_id": hotel_id,
                "hotel_name": hotel_name,
                "hotel_address": hotel_address,
                "hotel_longitude": hotel_longitude,
                "hotel_dimension": hotel_dimension,
                "hotel_image": hotel_image,
                "hotel_grade": hotel_grade.strip(),
                "hotel_phone": hotel_phone,
            }
            self.requests_room_info(hotel_info, beginDate, endDate)


if __name__ == '__main__':
    hotel = GetHotel()
    hotel.requests_hotel_API('beijing', '0100', 1)
