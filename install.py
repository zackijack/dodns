#!/usr/bin/env python3


from configparser import ConfigParser


def main():
    config = ConfigParser()
    config['settings'] = {}
    print("Please enter your DigitalOcean personal access token (with write privilege).")
    print("If you don't have, generate here: https://cloud.digitalocean.com/settings/api/tokens/new")
    config['settings']['token'] = input("Token: ")
    print("Please enter your domain(s) with format: subdomain>domain")
    print("e.g: sub>example.com")
    print("for 'sub.example.com' where 'example.com' is your domain, and 'sub' is an 'A' record under the domain")
    config['settings']['domains'] = input("Domains (separate with comma): ")
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main()
