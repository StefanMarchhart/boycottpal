import base64
import hashlib
import hmac
import json as simplejson
import time

DISQUS_SECRET_KEY = 'rTezDfnlsdYUX90sKTExhQWDERK48NYvG4MKgcalq03xK2acFt6Z22spQMkswFTt'
DISQUS_PUBLIC_KEY = 'UCkYzgSPnP4OtgopaqnhrhMrQnL6a8hJBvfzslmbB80N1jCaTexRI7mmVBumkoBO'


def get_disqus_sso(user_id=None, username=None, email=None):
    if user_id:
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
        }
    else:
        user_data = {}
    # create a JSON packet of our data attributes
    data = simplejson.dumps(user_data).encode('utf-8')
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = str(int(time.time()))
    key=bytes(DISQUS_SECRET_KEY,"utf-8")
    # generate our hmac signature
    # sig = hmac.HMAC(key, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    sig = hmac.HMAC(key, (str(message) +" "+ timestamp).encode(), hashlib.sha1).hexdigest()
    # sig = hmac.new(DISQUS_SECRET_KEY, (str(message) +" "+ timestamp).encode(), hashlib.sha1).hexdigest()

# return a script tag to insert the sso message
    return """
            this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
    """ % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=DISQUS_PUBLIC_KEY,
    )