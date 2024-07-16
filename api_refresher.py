import json
import requests
import secrets


CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token() -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'refresh_token': 'def50200d2358c90e06c14c4cece04bb5e1429219f72800c61571a046d41c78243d424dc9131ee1e3297bfc8da63cc41f812bf34513b5aaa7bc367d030674675a366c763d22a40ad4406660e80e03a4573b788f315639bed6adc12a9c751ebeabbd16a0aed9bb1d57279cdcb828a1af862a08f35fa248ced869b75ecfcec61b0caaf615aa2cff5204d7c8d9786eb77041a54851eb146d44126c3af65f20ae0d6f58b7c9258cd9cebf2dc6482c6674843a58b5abaad1b785f95a7ef4874bae01f6f0eb674da1a8732ae5cf85af01d2085c61ceed9596b31a056d1feb0c264956eb1c21932e9ac7183dfd918bda2f5318d15f1e3fbb1dbdfa963e3a282c9ee6e92295c383a530889541a28d3cce48a67c68b1d415ca591700c0fcd0de9aaf478489bd3c09b80168a272d8dc352aa782dd030ed22953b2be3f63d037dc119555bb501720420de46bb0e90fd0b7d2345ec5ce5e8631447fcc7c2f28de0c2f4aec7a95e15bc508b58bfbf9c266a11fa77e8a78fa3326114b842422a620b6e928fb77fb181ca4e1fd6f965'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        })
    
    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")


if __name__ == '__main__':
    token = generate_new_token()

    print_user_info(token['access_token'])
