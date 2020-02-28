[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# Overview

Creates google tag with a google analytics tracking id and generates the scripts tag.

## Directory structure

```
.
├── Pulumi.yaml
├── README.md
├── pulumi
│   ├── __main__.py
│   ├── dynamic_providers
│   │   └── google
│   │       ├── api_wrapper.py
│   │       └── tag_manager.py
│   ├── stacks
|   ├   └──pulumi.dev.yaml
│   ├── tag_manager.py
│   └── utils.py
├── requirements.txt
```


### Setup

1. Create a Python virtualenv, activate it, and install dependencies:

```
$ virtualenv -p python3 venv
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
2. Create the required stacks

```
$ pulumi stack init dev
```

3. Configure variables

```
$ pulum stack select core
$ pulumi config set aws:region <region>
$ pulumi config set google_api_key_file <google-api-key-file>
$ pulumi config set gtm_account_id <google-tag-manager-account-id>
```

4. Edit ```__main__.py``` file with acordingly.

###  Deploy
```
$ pulumi up

```


### Clean up

Destroy the stack and google tag manager resources.

```
$ pulumi destroy
$ pulumi stack rm
```
