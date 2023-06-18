import requests, json

def check_license(license_key):
    def get_license(license_key):
        API_KEY = 'sk_K4fcYyymjDSvOnhHxDyAxkALrximnFGskIMikXV6PCADAUPd4j1LQ5xx9LW0YNqx'
        headers = {
            'Authorization': f'Bearer {API_KEY}'
        }

        req = requests.get(f'https://api.hyper.co/v6/licenses/{license_key}', headers=headers)
        if req.status_code == 200:
            return req.json()
            
        return None

    license_data = get_license(license_key)
    
    if license_data:
        if license_data.get('metadata') != {}:
            print('License is already in use on another machine!')
        else:
            API_KEY = 'sk_K4fcYyymjDSvOnhHxDyAxkALrximnFGskIMikXV6PCADAUPd4j1LQ5xx9LW0YNqx'
            headers = {
                'Authorization': f'Bearer {API_KEY}'
            }

            LICENSE_KEY = license_key
            req = requests.get(f'https://api.hyper.co/v6/licenses/{LICENSE_KEY}', headers=headers)
        
            if req.status_code == 200:
                jsonres = (req.json())
                global username
                try:
                    username = (((jsonres['integrations'])['discord'])['username'])
                except:
                    username = 'Null'

                if jsonres['status'] == 'active' or jsonres['status'] == 'trialing':
                    authorized = 'Validated'
                    
                    infojson = {
                        "authorized": authorized ,
                        "discord": username,
                        "member_role": ""
                    }

                    return infojson

            else:
                return authorized 
        
    else:

        infojson = validate_key(license_key)
        return infojson


def validate_key(license_key):

    url = f"https://api.whop.com/api/v2/memberships/{license_key}"

    payload = json.dumps({
    "metadata": {
        "nocto": 'service'
    }
    })
    headers = {
    'Authorization': 'Bearer nqlCDiWLShoUAJMCdn6YQwZxFHo8SY5MlTmYYqRPKzU',
    'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    try:
        if response.json()['status'] == 'active' or response.json()['status'] == 'completed':
            print('Verified License!')
    except:
        infojson = {
            "authorized": "Not Validated",
            "discord": "null",
        } 
        return infojson

    userid = response.json()['user']
    discord_response = requests.get(f'https://api.whop.com/api/v2/members/{userid}', headers=headers)
    try:
        username = discord_response.json()['social_accounts'][0]['username']
    except: 
        username = discord_response.json()['username']

    infojson = {
        "authorized": "Validated",
        "discord": username,
    }

    return infojson
        
