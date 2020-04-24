import pulumi
from pulumi.resource import ResourceOptions

from pulumi_google_analytics.dynamic_providers import (WebProperty,
                                                       WebPropertyArgs)
from pulumi_google_tag_manager.dynamic_providers import (Container,
                                                         ContainerArgs,
                                                         Workspace,
                                                         WorkspaceArgs)
from pulumi_google_tag_manager.dynamic_providers.custom_event_trigger import \
    CustomEventTrigger
from pulumi_google_tag_manager.dynamic_providers.custom_html_tag import (
    CustomHtmlTag, CustomHtmlTagArgs)
from pulumi_google_tag_manager.dynamic_providers.data_layer_variable import \
    DataLayerVariable
from pulumi_google_tag_manager.dynamic_providers.ga_event_tag import GAEventTag
from pulumi_google_tag_manager.dynamic_providers.ga_pageview_tag import (
    GAPageviewTag)
from pulumi_google_tag_manager.dynamic_providers.pageview_trigger import \
    PageviewTrigger
from pulumi_google_tag_manager.dynamic_providers.publish import Publish

from pulumi_google_tag_manager.dynamic_providers.version import Version


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

pageview_trigger = PageviewTrigger("example-pageview-trigger",
    trigger_name="my-pageview-trigger",
    workspace_path=workspace.path
)

# creates GA pageview tag inside workspace
pageview_tag = GAPageviewTag(
    "example-pageview-tag",
    workspace_path=workspace.path,
    tag_name="my-pageview-tag",
    tracking_id=web_property.tracking_id,
    firing_trigger_id=pageview_trigger.trigger_id
)

custom_event_trigger = CustomEventTrigger("custom-event-trigger",
    trigger_name="my-event-trigger",
    workspace_path=workspace.path
)

# creates GA event tag inside workspace
event_tag = GAEventTag(
    "example-event-tag",
    workspace_path=workspace.path,
    tag_name="test event tag",
    tracking_id=web_property.tracking_id,
    event_category="test_category",
    event_action="{{Event}}",
    event_value="test_value",
    firing_trigger_id=custom_event_trigger.trigger_id
)

# creates custom HTML tag inside workspace
custom_tag = CustomHtmlTag(
    "example-custom-tag",
    args=CustomHtmlTagArgs(
        workspace_path=workspace.path,
        tag_name="hello world custom tag",
        html="<p>This is a test</p>",
        firing_trigger_id=[custom_event_trigger.trigger_id]
    ),
)

variable = DataLayerVariable("data-layer-var",
    variable_name="my-dl-var",
    workspace_path=workspace.path
)

publish = Publish("publish",
    workspace_path=workspace.path,
    opts=ResourceOptions(depends_on=[
        container, workspace, pageview_trigger, pageview_tag, custom_event_trigger, custom_tag, event_tag, variable
    ])
)

pulumi.export("container_id", container.container_id)
pulumi.export("custom_event_trigger_id", custom_event_trigger.trigger_id)
pulumi.export("data_layer_variable_id", variable.variable_id)
pulumi.export("gtm_tag", container.gtm_tag)
pulumi.export("gtm_tag_no_script", container.gtm_tag_noscript)
pulumi.export("container_version_path", publish.container_version_path)
