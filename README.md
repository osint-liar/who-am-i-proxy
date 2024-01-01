# Who Am I Proxy
An HTTP Proxy for [Who Am I Chrome extension](https://chromewebstore.google.com/detail/who-am-i/gdnhlhadhgnhaenfcphpeakdghkccfoo).
This small proxy script will greatly improve your results when enumerating across the different social media
platforms. It improves the results by using an origin header value, that the host server is expecting. 

This functionality is still in development.  

## Installing & Running
```shell
git clone https://github.com/osint-liar/who-am-i-proxy.git
cd who-am-i-proxy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python who-am-i-proxy.py
```
