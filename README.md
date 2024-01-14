# hh-cli

### Install dependencies

```shell
poetry install
```

### Generate Certificates

```shell
mkdir cert
cd cert
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Run CLI

```
python3 hh.py oauth --client-id "" --client-secret ""
```