# Vultr Dynamic DNS

### Use [vultr.com](https://www.vultr.com/)'s free DNS hosting as your own free private dynamic DNS provider - **using any TLD you own!**

---

#### How To:
* Install Python 3  - https://www.google.com.au/webhp?q=how%20to%20install%20python%203
* Create an account at [Vultr.com](https://www.vultr.com) (if you haven't already)
* Log in and go to the DNS tab
* Add your root domain and give it an IP - 192.168.1.1 will do just fine, the script will update it (if you choose to use your root domain as your Dynamic DNS domain)
  * [optional] Within that root domain, add a new subdomain A record that will serve as your Dynamic DNS domain
    * You'll need to give it an IP - 192.168.1.1 will do just fine, the script will update it
* (Outside of Vultr) Set your root domain's nameservers to ns1.vultr.com and ns2.vultr.com (Ask your domain registrar for how to do this)
* (Back in Vultr) Click on your username (top right) and go to the API menu option
* Enable API access and generate an API Key
  * Underneath 'Access Control' click 'Allow All IPv4' - this is essential as your IP is obviously undetermined (hence why you are using the script..)
  * If you enabled IPv6 for your instance and your host OS prefers IPv6, you may need to click "Allow All IPv6"
* Copy your API key into the update script 'api_key' variable
* Enter your root domain into the update script 'root_domain' variable
* Enter your subdomain the update script 'target_record' variable, or leave it blank id you are using your root domain for your Dynamic DNS
* Save that shiz and run the following in your terminal/Windows wannabe blackbox:

> python update.py

---

#### Log your output to Slack
If you use Slack you can send your updates to a Slack Channel using [Incoming Webhooks](https://api.slack.com/incoming-webhooks)
Just add your webhook URL into the *slack_webhook_url* variable and you will get notified when your IP changes, or if any errors occurred while updating

---

#### Automate for realz:
If your using a *nix system, add this to your crontab to update every hour:
> 0 * * * * python /path/to/where/you/saved/update.py >/dev/null 2>&1


If your not using a *nix system, start using a *nix system; Alternatively, look elsewhere for Windows help, you won't find it here.
