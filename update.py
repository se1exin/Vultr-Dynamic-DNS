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

# Slack webhook URL for logging. Leave blank if you don't want to use it.
slack_webhook_url = ''

def slack_log(message):
    '''Wrapper function for POSTing strings to a Slack incoming webhook'''

    print(message)  # print to console for normal logging

    if slack_webhook_url != '':
        # Format the message
        message = "Vultr Dynamic DNS\n" + "```" + message + "```"
        payload = {'text': message}
        
        req = urllib.request.Request(slack_webhook_url)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, json.dumps(payload).encode('utf-8'))

# ---------------------------------------------------

# START YOUR ENGINES!!!

# First up find our public IP address
ip_request = urllib.request.Request(ipify_url)
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
                found_record = record

    if found_record is not False:
        if found_record['data'] != public_ip: # Only update if the IP has changed
            # now update the zone record
            values = {
                'domain': root_domain,
                'RECORDID': found_record['RECORDID'],
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
                    slack_log('Updated ' + target_record + '.' + root_domain + ' to new IP ' + public_ip)
            except Exception as err:
                error_msg = 'Failed to update ' + target_record + '.' + root_domain
                error_msg += "\nIf you can't figure this one out, please lodge an issue at https://github.com/se1exin/Vultr-Dynamic-DNS with the following error details:\n"
                error_msg += str(err)
                slack_log(error_msg)
    else:
        slack_log('Could not find a matching record for subdomain ' + target_record + '.' + root_domain)
else:
    slack_log('Could not determine public address! You should probs check your Internet connection..')
