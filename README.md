VOIP.ms SMS-Email Gateway
=========================

Lets you send and receive SMS messages from your [VOIP.ms](https://voip.ms) account via email.

Requirements
------------

 * Python
 * A VOIP.ms account
 * A Mailgun account
 * A (sub)domain to send and receive emails with, set up with Mailgun

Setup
-----

1. Rename `settings.example.py` to `settings.py` and fill in the blanks as directed.
1. Set up the web server at, say, `sms.yoursite.com`.
1. Add `https://sms.yoursite.com/hook/< HOOK_URL_KEY >/sms?to={TO}&from={FROM}&message={MESSAGE}&id={ID}&date={TIMESTAMP}` as an "SMS URL Callback" in the VOIP.ms DID settings, replacing `< HOOK_URL_KEY >` with the value from `settings.py`. Enable "URL Callback Retry" at the same time.
1. Add a catch-all route to the Mailgun domain, POSTing to `https://sms.yoursite.com/hook/< HOOK_URL_KEY >/email` performing the same replacement of `< HOOK_URL_KEY >`.

Usage
-----

New SMS messages will be sent to the email specified in `settings.py`. You can reply to these messages to reply to the SMS's sender. You can also initiate a conversation directly by sending a new email to `< recipient phone # >@youremaildomain.com`.
