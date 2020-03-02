[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# Overview

Creates google tag with a google analytics tracking id and generates the scripts tag.

## Directory structure

```
.
├── Pulumi.yaml
├── README.md
pulumi
│   ├── Pulumi.dev.yaml
│   ├── __main__.py
│   ├── dynamic_providers
│   │   ├── __init__.py
│   │   ├── ga
│   │   │   ├── __init__.py
│   │   │   ├── web_property.py
│   │   │   └── web_property_provider.py
│   │   ├── gtm
│   │   │   ├── __init__.py
│   │   │   ├── container.py
│   │   │   ├── container_provider.py
│   │   │   ├── tag.py
│   │   │   ├── tag_provider.py
│   │   │   ├── workspace.py
│   │   │   └── workspace_provider.py
│   │   ├── service.py
│   │   └── templates
│   │       ├── gtm_tag.html
│   │       └── gtm_tag_noscript.html
│   ├── secrets.json
│   └── tag_manager.py
├── requirements.txt
```


### Setup

1. Create a Python virtualenv, activate it, and install dependencies:

```
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
$ pulumi config set ga_account_id <google-analytics-manager-account-id>
$ pulumi config set gtm_account_id <google-tag-manager-account-id>
```

4. Edit ```__main__.py``` file acordingly.

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
