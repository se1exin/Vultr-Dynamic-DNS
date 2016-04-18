# Vultr Dynamic DNS

### Use [vultr.com](vultr.com)'s free DNS hosting as your own free private dynamic DNS provider - **using any TLD you own!**

**Note: currently only subdomains are supported (root domains have not been tested)*


---


#### How To:
* Install Python 3  - https://www.google.com.au/webhp?q=how%20to%20install%20python%203
* Create an account at [Vultr.com](vultr.com) (if you haven't already)
* Log in and go to the DNS tab
* Add your root domain and give it an IP
* Within that root domain, and a new subdomain A record that will serve as your Dynamic DNS domain
  * You'll need to give it an IP - 111.222.333.444 will do just fine, the script will update it
  * (Outside of Vultr) Set your root domain's nameservers to ns1.vultr.com and ns2.vultr.com (Ask your domain registrar for how to do this)
 * (Back in Vultr) Click on your username (top right) and go to the API menu option
 * Enable API access and generate an API Key
 * Copy your API key into the update script 'api_key' variable
 * Enter your root domain into the update script 'root_domain' variable
 * Enter your subdomain the update script 'target_record' variable
 * Save that shiz and run the following in your terminal/Windows wannabe blackbox:
 * > python update.py

##### Automate for realz:
If your using a *nix system, add this to your crontab to update every hour:
> 0 * * * * python /path/to/where/you/saved/update.py >/dev/null 2>&1

If your not using a *nix system, start using a *nix system; Alternatively, go find someone else on GitHub who cares how to one-line a scheduled task on NT