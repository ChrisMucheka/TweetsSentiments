import sys, tweepy

class Connection():
 def connection(self):
    access_token  =  "622906360-e6dIBC0oIDWP2GXhO6KYIGVd3gExnOiMfqb1mmUM"
    access_token_secret  =  "8sYrRbdJ6ZzaHX6ZoCQx1K3JNF7wv65fa3PFzA4XEw8yF"
    consumer_key  =  "Gbh036wNRda2EU6KpH9YyS7sn"
    consumer_secret  =  "m4upmcexHeM3jfCm1GjK8ygmkBiC3g0tqOSP9WoiTEGt5aVfn1"
    auth  =  tweepy. OAuthHandler (consumer_key, consumer_secret)
    auth.set_access_token ( access_token, access_token_secret )
    api = tweepy.API ( auth )
    return api