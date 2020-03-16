[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# pulumi-google-tag-manager

This project contains a pip packaged named `pulumi-google-tag-manager` which allows Google Tag Manager and Google Analytics resources to be managed in Pulumi.

An example Pulumi program which uses this package is present in the `example` folder.

## Prerequesits

* Install the package into your Pulumi project using `pip`
* Set your Google credentials in your stack config:

```
$ pulumi config set aws:region <region>
$ pulumi config set google_api_key_file <google-api-key-file>
$ pulumi config set ga_account_id <google-analytics-manager-account-id>
$ pulumi config set gtm_account_id <google-tag-manager-account-id>
```

You will need to ensure that your API key represents a service worker with Project Owner permissions, and that you have added this user to the GTM users.


## Directory structure

```
.
├── example
│   ├── __main__.py
│   ├── Pulumi.yaml
│   └── README.md
├── pulumi_google_tag_manager
│   └── dynamic_providers
│       ├── ga
│       │   ├── web_property_provider.py
│       │   └── web_property.py
│       ├── gtm
│       │   ├── container_provider.py
│       │   ├── container.py
│       │   ├── tag_provider.py
│       │   ├── tag.py
│       │   ├── workspace_provider.py
│       │   └── workspace.py
│       ├── service.py
│       └── templates
│           ├── gtm_tag.html
│           └── gtm_tag_noscript.html
├── README.md
├── requirements.txt
└── setup.py
```
