import requests

def footrpatrolOpenRaffles():

    url = 'https://mosaic-platform.jdmesh.co/stores/footpatrolgb/content?api_key=6048110e2d7e087082d9a8d1c07b9e2c&channel=iphone-mosaic'

    res = requests.get(url)
    jsonresponse= res.json()

    count = 0
    new_count = 0

    products_list = []

    for i in range(len(jsonresponse['products'])):

        if jsonresponse['products'][count]['status'] == 'available':
            name = jsonresponse['products'][count]['name']
            subname = jsonresponse['products'][count]['subTitle']

            print(str(new_count)+ '.', name, subname)
                
            products_list.append(jsonresponse['products'][count])

            new_count+=1

        count+=1

    print("")
    option = int(input('Option: '))
    sizes_list = (products_list[option]['options'])

    raffle_name = products_list[option]['name'] + ' ' + products_list[option]['subTitle']
    image = products_list[option]['mainImage']['original']
    
    product_id = str(products_list[option]['options'][0]['optionID']).split(':')[0]
    return product_id, sizes_list

def sizeOpenRaffles():

    url = 'https://mosaic-platform.jdmesh.co/stores/size/content?api_key=0ce5f6f477676d95569067180bc4d46d&channel=iphone-mosaic'

    res = requests.get(url)
    jsonresponse= res.json()

    count = 0
    new_count = 0

    products_list = []

    for i in range(len(jsonresponse['products'])):

        if jsonresponse['products'][count]['status'] == 'available':
            name = jsonresponse['products'][count]['name']
            subname = jsonresponse['products'][count]['subTitle']

            print(str(new_count)+ '.', name, subname)
                
            products_list.append(jsonresponse['products'][count])

            new_count+=1

        count+=1

    print("")
    option = int(input('Option: '))
    sizes_list = (products_list[option]['options'])

    raffle_name = products_list[option]['name'] + ' ' + products_list[option]['subTitle']
    image = products_list[option]['mainImage']['original']
    
    product_id = str(products_list[option]['options'][0]['optionID']).split(':')[0]
    return product_id, sizes_list