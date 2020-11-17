import requests, json
from fake_useragent import UserAgent


class GetCity:
    def __init__(self):
        self.url = "https://www.bthhotels.com/Ajax/GetCity_All"
        self.header = {
            'user-agent': UserAgent().Chrome
        }

    def candle_response(self, json_data):
        data = json_data['data']
        result = [
            {
                'cityId': item['CD'],
                'cityName': item['Descript'],
                'cityCode': item['Pinyin'],
                'pageNo': (int(item['Hotelnum']) // 15 + 1)
            }
            for item in data]
        with open('city.json', 'w', encoding='utf-8') as f:
            json_file_content = [{'cityId': item['cityId'], 'cityName': item['cityName']} for item in result]
            json_file_content = str(json_file_content).replace("'", '"')
            f.write(json_file_content)
        return result

    def request_API(self):
        response = requests.get(self.url, headers=self.header)
        json_data = json.loads(response.text)
        return self.candle_response(json_data)


if __name__ == '__main__':
    city = GetCity()
    city.request_API()
