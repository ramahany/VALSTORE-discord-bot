import re
import asyncio
import os
import requests
import json
import discord
import base64


def get_guns_dic():

    # ---------get version -----------#
    version_session = requests.session()
    v = version_session.get('https://valorant-api.com/v1/version')
    # print(v.status_code)
    client_version = v.json()['data']['riotClientVersion']
    # print(client_version)
    client_platform = 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    headers = {
        'X-Riot-ClientVersion': client_version,
        'X-Riot-ClientPlatform': client_platform,
        "Content-Type": "application/json",
        "Accept-Language": "en-US",
        'User-Agent': 'RiotClient/60.0.3.4751956.4749685 rso-auth (Windows;10;;Professional, x64)'
    }
    content = version_session.get('https://valorant-api.com/v1/weapons')
    print('store loaded correctly')
    guns = content.json()['data']
    guns_dic = {'gun_id': ['gun_name', 'gun_img_link']}

    for item in guns:
        for w in item['skins']:
            guns_dic[w['levels'][0]['uuid']] = [w['levels'][0]['displayName'], w['levels'][0]['displayIcon']]

    return guns_dic


def get_store(username, password):
        headers = {
            "Content-Type": "application/json",
            "Accept-Language": "en-US",
            'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)'
        }

        data = {
            "client_id": "play-valorant-web-prod",
            "nonce": "1",
            "redirect_uri": "https://playvalorant.com/opt_in",
            "response_type": "token id_token",
            "scope": "account openid"
        }
        session = requests.session()
        session.headers.update(headers)
        r = session.post('https://auth.riotgames.com/api/v1/authorization', json=data)
        print(r.status_code)
        data = {
            'type': 'auth',
            "username": username,
            "password": password,
            "remember": True,
            "language": "en_US"
        }
        rend = session.put('https://auth.riotgames.com/api/v1/authorization', json=data)
        dt = rend.json()
        print(rend.status_code)

        pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        dt = pattern.findall(dt['response']['parameters']['uri'])[0]
        access_token = dt[0]
        id_token = dt[1]
        expires_in = dt[2]

        print(access_token)

        # print(access_token)
        # print(f' expires_in : {expires_in}')

        headers = {
            'Authorization': f'Bearer {access_token}',
            "Content-Type": "application/json",
            "Accept-Language": "en-US",
            'User-Agent': 'RiotClient/60.0.3.4751956.4749685 rso-auth (Windows;10;;Professional, x64)'
        }
        session.headers.update(headers)
        r = session.post('https://entitlements.auth.riotgames.com/api/token/v1')
        print(r.json())
        entitlements_token = r.json()['entitlements_token']
        # print(entitlements_token)
        r = session.get('https://auth.riotgames.com/userinfo')
        # print(r.status_code)
        player_id = r.json()['sub']
        # print(player_id)
        # ------------------ now we have the entitlements_token and the player_id ------------------ #
        headers['X-Riot-Entitlements-JWT'] = entitlements_token
        session.headers.update(headers)
        region = 'eu'
        store_url = f'https://pd.{region}.a.pvp.net/store/v2/storefront/{player_id}'
        r = session.get(store_url)
        # print(r.status_code)
        store = r.json()['SkinsPanelLayout']['
SingleItemOffers']
        time_remaining_in_seconds = r.json()['SkinsPanelLayout']['SingleItemOffersRemainingDurationInSeconds']
        # print(store)
        wallet_url = f'https://pd.{region}.a.pvp.net/store/v1/wallet/{player_id}'
        r = session.get(wallet_url)
        # print(r.status_code)
        valorant_points = r.json()['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
        # print(valorant_points)
        return store, valorant_points
