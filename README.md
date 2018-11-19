### CryptoBackend

A simple Python/Flask backend providing json data to the frontend apps to build
charts from a datalog file.

Note: A very simple front is also provided in the web directory for testing purpose only.


```
python3 cryptobackend.py
cd web ; python3 -m http.server 8000 
```

While developping, you may need the following Firefox plugin : CORS Everywhere (by Spenibus) 

In production, I use nginx as reverse proxy.

nginx : ''/etc/nginx/sites-enabled/default''

```
         # CryptoBackEnd
         location /cryptoback/ {
                  proxy_set_header Host $host;
                  proxy_set_header X-real-IP $remote_addr;
                  proxy_pass http://127.0.0.1:5000;
          }
```

