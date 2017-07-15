#!/usr/bin/env python3


from os import path
from datetime import datetime
from configparser import ConfigParser

try:
    from requests import put, get
except:
    print("Seems you forgot to install python modules.")
    print("Run: `pip install -r requirements.txt`")
    raise


API_URL = "https://api.digitalocean.com/v2/domains/"
CHECK_IP = "https://api.ipify.org"


def main():
    config = ConfigParser()
    config.read(path.join(path.dirname(__file__), 'config.ini'))

    token = config['settings']['token']
    domains = [domain.strip() for domain in config['settings']['domains'].split(',')]

    try:
        for domain in domains:
            now = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            ip = update_ip(token, domain)
            if ip:
                print(now, domain + ": from " + ip['domain'] + " to " + ip['device'])
    except:
        now = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        print(now)
        raise


def get_record_id(token, domain):
    subdomain = None

    if len(domain.split('>')) > 1:
        subdomain = domain.split('>')[0]
        domain = domain.split('>')[1]

    url = API_URL + "%s/records" % domain
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer %s" % token
    }

    response = get(url, headers=headers).json()

    if subdomain is None:
        record = [record for record in response['domain_records']
                  if record['type'] == "A" and record['name'] == "@"][0]
    else:
        record = [record for record in response['domain_records']
                  if record['type'] == "A" and record['name'] == subdomain][0]

    return record


def update_ip(token, domain):
    record = get_record_id(token, domain)
    ip = {
        "domain": record['data'],
        "device": get(CHECK_IP).text
    }
    response = None
    domain = domain.split('>')[1] if len(domain.split('>')) > 1 else domain

    if ip['domain'] != ip['device']:
        record_id = str(record['id'])
        url = API_URL + "%s/records/%s" % (domain, record_id)
        payload = '{"data": "%s"}' % ip['device']
        headers = {
            "content-type": "application/json",
            "authorization": "Bearer %s" % token
        }

        response = put(url, data=payload, headers=headers).status_code

    if response == 200:
        return ip

    return False


if __name__ == "__main__":
    main()
