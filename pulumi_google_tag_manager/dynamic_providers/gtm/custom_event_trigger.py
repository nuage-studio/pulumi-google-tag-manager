from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.gtm.custom_event_trigger_provider import \
    CustomEventTriggerProvider
from pulumi_google_tag_manager.dynamic_providers.service import \
    get_key_file_location


class CustomEventTrigger(Resource):
    """
    Represents a custom event trigger, which can be triggered using the `dataLayer`. 
    See https://support.google.com/tagmanager/answer/7679219?hl=en
    """
    path: Output[str]
    trigger_id: Output[str]

    def __init__(self,
            name: Input[str],
            trigger_name: Input[str],
            workspace_path: Input[str],
            opts=None):
        super().__init__(CustomEventTriggerProvider(), name, {
            "trigger_name": trigger_name,
            "key_location": get_key_file_location(),
            "workspace_path": workspace_path,
            "path": None,
            "trigger_id": None
        }, opts)
