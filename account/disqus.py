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
    data = simplejson.dumps(user_data)

    b64_data = str(base64.b64encode(data.encode('utf-8')),'utf-8')

    timestamp = str(int(time.time()))
    # encode the data to base64
    message = b64_data+' '+timestamp
    message = message.encode()
    # generate a timestamp for signing the message
    key=bytes(DISQUS_SECRET_KEY,"utf-8")
    # generate our hmac signature

    # sig = hmac.HMAC(key, (str(message) +" "+ timestamp).encode(), hashlib.sha1).hexdigest()
    sig = hmac.new(key, message, hashlib.sha1).hexdigest()
    # import ipdb; ipdb.set_trace()


# return a script tag to insert the sso message
    return """
            this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
    """ % dict(
        message=b64_data,
        timestamp=timestamp,
        sig=sig,
        pub_key=DISQUS_PUBLIC_KEY,
    )