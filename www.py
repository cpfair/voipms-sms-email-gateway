from flask import Flask, request
import requests
from settings import HOOK_URL_KEY, APPROVED_SENDERS, APPROVED_PASSPHRASE, \
                     VOIPMS_EMAIL, VOIPMS_API_PASSWORD, VOIPMS_OUTGOING_DID, \
                     MAILGUN_API_KEY, EMAIL_DOMAIN

app = Flask(__name__)

assert HOOK_URL_KEY, "HOOK_URL_KEY must be set to a random string"

def send_email(from_addr, to_addr, subject, body):
    res = requests.post("https://api.mailgun.net/v3/%s/messages" % EMAIL_DOMAIN,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": from_addr,
            "to": to_addr,
            "subject": subject,
            "text": body
        })
    assert res.status_code == 200, "Mailgun send request failed - %d %s" % (res.status_code, res.text)

@app.route("/hook/%s/email/" % HOOK_URL_KEY, methods=["POST"])
def hook_email():
    # Top security.
    if request.form["sender"] not in APPROVED_SENDERS:
        return ""
    to_mt = request.form["recipient"].split("@")[0]
    message = request.form["stripped-text"]

    # Extra top security.
    if APPROVED_PASSPHRASE:
        if APPROVED_PASSPHRASE not in message:
            send_email("system@%s" % EMAIL_DOMAIN,
                       request.form["sender"],
                       "SMS send failure to %s" % to_mt,
                       "Incorrect passphrase provided")
            return ""
        message = message.replace(APPROVED_PASSPHRASE, "").strip()

    post_data = {
        "api_username": VOIPMS_EMAIL,
        "api_password": VOIPMS_API_PASSWORD,
        "method": "sendSms",
        "did": VOIPMS_OUTGOING_DID,
        "dst": to_mt,
        "message": message
    }
    res = requests.post("https://voip.ms/api/v1/rest.php", data=post_data)
    if res.status_code != 200 or res.json()["status"] != "success":
        send_email("system@%s" % EMAIL_DOMAIN,
                   request.form["sender"],
                   "SMS send failure to %s" % to_mt,
                   "VOIP.ms API returned an error:\n%s" % res.text)

@app.route("/hook/%s/sms/" % HOOK_URL_KEY, methods=["GET"])
def hook_sms():
    from_mt = request.args["FROM"]
    message = request.args["MESSAGE"]
    ts = request.args["TIMESTAMP"]
    send_email("%s@%s" % (from_mt, EMAIL_DOMAIN),
               APPROVED_SENDERS[0],
               "SMS from %s" % from_mt,
               "%s\nReceived at %s" % (message, ts))
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
