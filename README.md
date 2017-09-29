# TwoCaptcha - Wrapper
TwoCaptcha - Wrapper is a wrapper for the 2Captcha API (Recaptcha V2 Token method only) that solves your CAPTCHA with high accuracy.

## Intallation

### pip
```
pip install twocaptcha
```

### Source
```
git clone https://github.com/tiagocardosoweb/twocaptcha-wrapper.git
cd twocaptcha
python setup.py install
```

## How to start?
First you need a 2Captcha Account, you can [Register Here](https://2captcha.com?from=4489829), after register your account:
* Login into your account.
* Add some money.
* Go to "2Captcha API"
* Get "CAPTCHA Key"

# Usage

## Getting your balance
```
from twocaptcha import TwoCaptcha

two= TwoCaptcha(<api_key>, <soft_id=None>, <log=None>)
print two.get_balance()

This function will return your account balance (string).
```

## Uploading a captcha
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>)
print two.upload(<google_key>,<page_url>)

This function will upload the captcha request and then return the request ID (string).
```

## Response from a captcha
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>)
print two.get_response(<request_id>,<except=False>)

This function will request the token from the a request and return you the resolution token (string).
**NOTE:** If you want the method to raise an exception in case something goes wrong, set <except> to *True*
```

## Solving a captcha
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>>)
print two.resolve_captcha(<google_key>,<page_url>,<waittime=15>)

This function will upload the captcha request & ask back the captcha solution and return the token (string).
*How it works?* 15 seconds timeout + (5 seconds timeout * while token is not returned )
```

## Solving a captcha via Pingback
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>, <extra_data_file_path=None>)
print two.upload(<google_key>,<page_url>,<pingback_url>)

This function will upload the captcha request and then return it via a POST request to your Pingback URL.
```


## Adding a Pingback URL
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>, <extra_data_file_path=None>)
print two.add_pingback(<url>)
```

## Getting your Pingback List
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>)
print two.add_pingback(<url>)
```

## Deleting a Pingback URL
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=None>)
print two.delete_pingback(<url=None>, <all=False>)

You must provie and URL or set <all> to *True*
```

## Complain
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=Log Here>)
print two.complain(<request_id>)
```

## Logger
```
from twocaptcha import TwoCaptcha

two = TwoCaptcha(<api_key>, <soft_id=None>, <log=Log Here>)
print two.getbalance()
```

## Exceptions
```
All methods throw up exceptions, so be sure to import them

from twocaptcha import AccessDeniedException 

 - AccessDeniedException 
 - CaptchaException
 - BalanceException
 - PingbackException
 - KeyException

```
