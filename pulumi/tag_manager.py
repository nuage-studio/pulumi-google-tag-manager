import pulumi
from dynamic_providers.google.tag_manager import GTagManager, GTagManagerArgs

config = pulumi.Config()

secret_file = config.require('google_api_key_file')

gtm_manager = GTagManager(
    name='test',
    args=GTagManagerArgs(
        account_id=config.require('gtm_account_id'), # google tag manager account id
        container_name='hello-world-container', # container name
        workspace_name='hello-world-workspace', # workspace name
        tag_name='hello-world', # name of the tag
        site_name='example.com', # site_name for google analytics
        site_url='https://example.in', # site_url for google analytics
        key_file=secret_file # path of google api secret key file
    )
)

pulumi.export('container_id', gtm_manager.container_id)
pulumi.export('script_tag', gtm_manager.script_tag)
