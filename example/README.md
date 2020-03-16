# pulumi-google-tag-manager Example

This folder contains an example Pulumi program which creates GTM resources.

### Setup

1. Create a Python virtualenv, activate it, and install the pip project from the parent folder:

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -e ..
```
2. Create the required stacks

```
$ pulumi stack init dev
```

3. Configure variables

```
$ pulumi config set aws:region <region>
$ pulumi config set google_api_key_file <google-api-key-file>
$ pulumi config set ga_account_id <google-analytics-manager-account-id>
$ pulumi config set gtm_account_id <google-tag-manager-account-id>
```

You will need to ensure that your API key represents a service worker with Project Owner permissions, and that you have added this user to the GTM users.

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
