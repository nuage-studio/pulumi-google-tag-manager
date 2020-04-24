from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.pageview_trigger_provider import \
    PageviewTriggerProvider

from ..service import get_key_file_location
from .custom_event_trigger_provider import CustomEventTriggerProvider


class PageviewTrigger(Resource):
    """
    Represents Pageview GTM trigger. 
    See https://support.google.com/tagmanager/answer/7679319?hl=en
    """
    path: Output[str]
    trigger_id: Output[str]
    trigger_name: Output[str]

    def __init__(self,
            name: Input[str],
            trigger_name: Input[str],
            workspace_path: Input[str],
            opts=None):
        super().__init__(PageviewTriggerProvider(), name, {
            "trigger_name": trigger_name,
            "key_location": get_key_file_location(),
            "workspace_path": workspace_path,
            "path": None,
            "trigger_id": None
        }, opts)
