# Email to send and receive email on - registered in Mailgun.
EMAIL_DOMAIN = "your.domain.com"

# Only accept outgoing messages from this address.
# Incoming messages are sent to the first in this list.
APPROVED_SENDERS = ("your@email.com",)

# Only accept outgoing messages containing this passphrase
# (which will be stripped before sending).
APPROVED_PASSPHRASE = "penguins"

# DID to send SMSes from.
VOIPMS_OUTGOING_DID = "1234567890"

# API URLs are of form /hook/HOOK_URL_KEY/sms.
# This should be random.
HOOK_URL_KEY = ""

# Visit https://voip.ms/m/api.php to set up your API password.
# You must also add your web server's IP as an authorized API user.
VOIPMS_EMAIL = "your@email.com"
VOIPMS_API_PASSWORD = ""

# Accessible from the Mailgun dashboard.
MAILGUN_API_KEY = ""
