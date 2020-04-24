from pulumi import Input, Output
from pulumi.dynamic import Resource
from .ga_event_tag_provider import GAEventTagProvider

from ..service import get_key_file_location
from .ga_pageview_tag_provider import GAPageviewTagProvider
from typing import List

class GAEventTag(Resource):
    """
    Represents a Google Analytics UA tag in GTM which tracks events.
    """
    tag_id: Output[str]
    path: Output[str]

    def __init__(self,
            name: str,
            workspace_path: Input[str],
            tag_name: Input[str],
            tracking_id: Input[str],
            event_category: Input[str],
            event_action: Input[str],
            event_value: Input[str],
            firing_trigger_id: Input[List[str]] = [],
            opts=None):
        full_args = {
            "tag_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            "firing_trigger_id": firing_trigger_id,
            "workspace_path": workspace_path,
            "tag_name": tag_name,
            "tracking_id": tracking_id,
            "event_category": event_category,
            "event_action": event_action,
            "event_value": event_value
        }

        super().__init__(GAEventTagProvider(), name, full_args, opts)
