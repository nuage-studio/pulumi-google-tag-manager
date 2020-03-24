import pulumi
from pulumi_google_analytics.dynamic_providers import WebProperty, WebPropertyArgs
from pulumi_google_tag_manager.dynamic_providers import (
    Container,
    ContainerArgs,
    Tag,
    TagArgs,
    Workspace,
    WorkspaceArgs,
)
from pulumi_google_tag_manager.dynamic_providers.custom_html_tag import (
    CustomHtmlTag,
    CustomHtmlTagArgs,
)

config = pulumi.Config()

ga_account_id = config.require("ga_account_id")
gtm_account_id = config.require("gtm_account_id")

# create or fetch web-property
web_property = WebProperty(
    "example-web_property",
    args=WebPropertyArgs(
        account_id=ga_account_id,
        site_name="example.com",
        site_url="https://example.com",
    ),
)

# create gtm container
container = Container(
    "example-container",
    args=ContainerArgs(
        account_id=gtm_account_id, container_name="hello world container"
    ),
)

# create workspace inside the container
workspace = Workspace(
    "example-workspace",
    args=WorkspaceArgs(
        container_path=container.path, workspace_name="hello world workspace"
    ),
)

# creates gtm tag inside workspace
tag = Tag(
    "example-tag",
    args=TagArgs(
        workspace_path=workspace.path,
        tag_name="hello world tag",
        tracking_id=web_property.tracking_id,
    ),
)

# creates custom HTML tag inside workspace
custom_tag = CustomHtmlTag(
    "example-custom-tag",
    args=CustomHtmlTagArgs(
        workspace_path=workspace.path,
        tag_name="hello world custom tag",
        html="<p>This is a test</p>",
    ),
)

pulumi.export("container_id", container.container_id)
pulumi.export("gtm_tag", container.gtm_tag)
pulumi.export("gtm_tag_no_script", container.gtm_tag_noscript)
