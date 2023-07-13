import requests, re, csv, json, xmltodict, time
import urllib.parse

from lxml import html
from lxml import etree


token = "5440c056580b44b5b2e8f33a2458f23bc2c96db0c04"
header = {
    "user-agent": "Mozilla/5.0"
}     
column_header = ['Product_Name', 'Brand', 'Pounds',  'Rands', 'Description', 'Image1', 'Image2', 'Image3', 'Technical Details', 'Sub_Category_1', 'Sub_Category_2', 'urls']

with open('AWS_data_sc.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(column_header)

    with open('13114_pro.csv', 'r', encoding='utf-8-sig') as f:
        column = csv.reader(f, delimiter=',')
        images_listing, description = [], []
        for row in column:
            url_ = ''.join(row)
            targetUrl = urllib.parse.quote(url_)
            url = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                print(response)
                data = response.content
                source_code = html.fromstring(data)
                product_name = source_code.xpath("//span[@id='productTitle']")[0].text
                brand = source_code.xpath("//span[@id='productTitle']")[0].text.split()[0]
                xmlstr = etree.tostring(source_code, pretty_print=True, encoding='unicode', method='xml')
                result = re.search('colorImages(.*)', xmlstr)
                res = json.dumps(result.group(1)[16:-2], sort_keys=True)
                respon = json.loads(r'{}'.format(res))
                images_list = json.loads(respon)

                for o in images_list: images_listing.append(o['hiRes'])
                image1, image2, image3 = images_listing[0], images_listing[1], images_listing[2]
                try:
                    if source_code.xpath("//span[@class='a-size-small a-color-secondary aok-align-center basisPrice']/child::text()[1]")[0] == 'RRP:         ':
                        print('RRP')
                        pounds = source_code.xpath("(//span[@class='a-price a-text-price']/span[1])[1]")[0].text.encode("ascii", "ignore").decode().replace('EUR', '').replace('\n', '.').replace('Â', '')
                        time.sleep(1)
                except Exception as e:
                    try:
                        result_pound = re.search('data-price-totals=(.*)', xmlstr)
                        resu = json.dumps(result_pound.group(1)[22:28], sort_keys=True)
                        pounds = re.sub(r'[\\u00&"a={}USD56ER11]', '', resu)
                    except Exception as e: pounds = ''
                try: rands = float(pounds) * 23 * 2.5 
                except: rands = ''
                for desc in source_code.xpath("//ul[@class='a-unordered-list a-vertical a-spacing-mini']/li/span"): description.append(desc.text)
                descriptions = ''.join(description)
                tab_head, tab_data = [], []
                for th in source_code.xpath("//th[@class='a-color-secondary a-size-base prodDetSectionEntry']"): tab_head.append(th.text.strip())
                for td in source_code.xpath("//td[@class='a-size-base prodDetAttrValue']"): tab_data.append(td.text.encode("ascii", "ignore").decode().strip())
                Details_ = []
                for i in range(1,13):
                    try: Details_.append(tab_head[i]+': '+tab_data[i])
                    except: Details_.append('')
                ddetails = ''.join(Details_)
                sub_category_list = []
                for category in source_code.xpath("//ul[@class='a-unordered-list a-horizontal a-size-small']/li/span/a"): sub_category_list.append(category.text.strip())
                try: sub_category_1 = sub_category_list[-1]
                except: sub_category_1 = ''
                try: sub_category_2 = sub_category_list[-2]
                except: sub_category_2 = ''
                Url_ = url_
                data_to_write = [product_name, brand, pounds, rands, descriptions, image1, image2, image3, ddetails, sub_category_1, sub_category_2, Url_]
                writer.writerow(data_to_write)
print('done')
