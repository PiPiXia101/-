import requests, json, datetime, time, execjs
from fake_useragent import UserAgent

today = datetime.datetime.now()
beginDate = today.strftime('%Y-%m-%d')
endDate = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def get_code(data):
    with open('code1.js', 'r', encoding='utf-8') as f:
        js_str = f.read()
    js_obj = execjs.compile(js_str)
    code = js_obj.call('abcdefg', data)
    print(code)


def requests_code_API(hotelIDs):
    data = {
        "detailRequest.bookingChannel": "1",
        "detailRequest.cardNo": "192928",
        "detailRequest.cheapestPriceFlag": "false",
        "detailRequest.checkInDate": beginDate,
        "detailRequest.checkOutDate": endDate,
        "detailRequest.crawledFlag": "0",
        "detailRequest.customerLevel": "11",
        "detailRequest.hotelIDs": hotelIDs,
        "detailRequest.interceptAction": "0",
        "detailRequest.isAfterCouponPrice": "true",
        "detailRequest.isDebug": "false",
        "detailRequest.isLogin": "false",
        "detailRequest.isMobileOnly": "false",
        "detailRequest.isNeed5Discount": "false",
        "detailRequest.isTrace": "false",
        "detailRequest.language": "cn",
        "detailRequest.needDataFromCache": "true",
        "detailRequest.needPromotion": "true",
        "detailRequest.orderFromID": "50",
        "detailRequest.payMethod": "0",
        "detailRequest.productType": "0",
        "detailRequest.promotionChannelCode": "0000",
        "detailRequest.proxyID": "ZD",
        "detailRequest.sellChannel": "1",
        "detailRequest.settlementType": "0",
        "detailRequest.updateOrder": "false",
        "_": int(round(time.time() * 1000)),
    }
    header = {
        'user-agent': UserAgent().Chrome
    }
    url = 'http://hotel.elong.com/ajax/detail/getcode.html'
    response = requests.get(url, headers=header, params=data)
    result = json.loads(response.text)

    with open('code1.js', 'r', encoding='utf-8') as f:
        js_str = f.read()
    js_obj = execjs.compile(js_str)
    with open('test.txt','w',encoding='utf-8') as f:
        f.write(result['value'])
    key= js_obj.call('abcdefg', result['value'], 'detail', beginDate, hotelIDs, endDate)
    print(key)


def requests_room_info(hotelIDs):
    data = {
        "bookingChannel": "1",
        "cardNo": "192928",
        "cheapestPriceFlag": "false",
        "checkInDate": beginDate,  # 入住时间
        "checkOutDate": endDate,  # 退房时间
        "crawledFlag": "0",
        "customerLevel": "11",
        "hotelIDs": hotelIDs,  # 酒店ID
        "interceptAction": "0",
        "isAfterCouponPrice": "true",
        "isDebug": "false",
        "isLogin": "false",
        "isMobileOnly": "false",
        "isNeed5Discount": "false",
        "isTrace": "false",
        "language": "cn",
        "needDataFromCache": "true",
        "needPromotion": "true",
        "orderFromID": "50",
        "payMethod": "0",
        "productType": "0",
        "promotionChannelCode": "0000",
        "proxyID": "ZD",
        "sellChannel": "1",
        "settlementType": "0",
        "updateOrder": "false",
        "code": "51652351",
    }
    header = {
        'user-agent': UserAgent().Chrome
    }
    url = 'http://hotel.elong.com/ajax/tmapidetail/gethotelroomsetjvajson'
    response = requests.post(url, headers=header, params=data)
    result = json.loads(response.text)
    with open('test.json','w',encoding='utf-8') as f:
        f.write(str(result['hotelInventory']['rooms']))
    for item in result['hotelInventory']['rooms']:
        room_id = item['roomTypeID']
        room_name = item['roomTypeName']
        room_bed = item['bedTypeName']
        room_window = '有' if not item['noWindow'] else '没有'
        try:
            room_window_type = item['windowTypeDescCn']
        except:
            room_window_type = '默认'
        room_area = item['area']
        room_images = [img['bigImage']['oldImageUrl'] for img in item['roomImageList']]
        room_price_num_rule = sorted([
            [
                '到店付款' if price['paymentType'] == 1 else '在线付款',
                price['priceOfDays'][0]['salePrice'],
                '不可取消' if price['cancelRuleType'] == 2 else price['cancelRuleDesc'],
                price['breakfastDesc'],
                '有房间' if price['roomNumStatus'] == 1 else '没有房间',
            ] for price in item['products']])
        for price_num_rule in room_price_num_rule:
            if '到店付款' in price_num_rule or '没有房间' in price_num_rule:continue
            pnr = price_num_rule
            break
        room_info = {
            "hotel_id":hotelIDs,
            "room_id": room_id,
            "room_name": room_name,
            "room_bed": room_bed,
            "room_window": room_window + ' ' + room_window_type,
            "room_area": room_area,
            # "room_images": room_images[0],
            "room_price": pnr[1],
            "room_num": pnr[-1],
            "room_rule":pnr[2]
        }
        print(room_info)
        print('-' * 10)
# data = requests_code_API('63887851')
strat_time = time.time()
requests_room_info('62687227')
print(time.time()-time.time())
