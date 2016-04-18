#!/usr/bin/python
import urllib.parse
import urllib.request
import json
import sys

# Vultr credentials and target DNS records
api_key = 'vultr_api_key'  # Update with Vultr API Key
root_domain = 'domain.com'  # Update with root domain name (e.g. 'domain.com')
target_record = ''  # Update with subdomain name (e.g. 'sub' - for sub.domain.com). Leave blank for root domain.
vultr_headers = {'API-key': api_key}

# Vultr Endpoints
list_url = 'https://api.vultr.com/v1/dns/records?domain=' + root_domain
update_url = 'https://api.vultr.com/v1/dns/update_record'

# Endpoint for retrieving our public IP address
ipify_url = 'https://api.ipify.org?format=json'

# These are needed later, and are instantiated as
# False to halt execution if something fails prematurely
public_ip = False
target_record_id = False

# START YOUR ENGINES!!!

# First up find our public IP address
ip_request = urllib.request.Request(ipify_url, None, vultr_headers)
with urllib.request.urlopen(ip_request) as list_response:
    ip_address = json.loads(list_response.read().decode('utf-8'))
    public_ip = ip_address['ip']

if ip_address is not False:
    # Now request a list of stored DNS records from Vultr to obtain the RECORDID for our target subdomain
    list_request = urllib.request.Request(list_url, None, vultr_headers)
    with urllib.request.urlopen(list_request) as list_response:
        zone_records = json.loads(list_response.read().decode('utf-8'))

        for record in zone_records:
            if record['name'] == target_record and record['type'] == 'A':

                # Now we have matched the subdomain we also hav it's RECORD ID.
                target_record_id = record['RECORDID']

    if target_record_id is not False:
        # now update the zone record
        values = {
            'domain': root_domain,
            'RECORDID': target_record_id,
            'name': target_record,
            'data': public_ip,
            'ttl': 120
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')

        update_request = urllib.request.Request(update_url, data, vultr_headers)
        try:
            with urllib.request.urlopen(update_request) as update_response:
                update_result = update_response.read()
                print('Updated ' + target_record + '.' + root_domain + ' to new IP ' + public_ip)
        except Exception as err:
            print('Failed to update ' + target_record + '.' + root_domain)
            print("If you can't figure this one out, please lodge an issue at https://github.com/se1exin/Vultr-Dynamic-DNS with the following error details:\n")
            print(err)
    else:
        print('Could not find a matching record for subdomain ' + target_record + '.' + root_domain)
else:
    print('Could not determine public address! You should probs check your Internet connection..')
