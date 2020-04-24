from pulumi.dynamic import Resource
from pulumi import Input, Output
from .ga_pageview_tag_provider import GAPageviewTagProvider
from ..service import get_key_file_location
from typing import List

class GAPageviewTag(Resource):
    """
    Represents a Google Analytics UA tag in GTM which tracks page views.
    """
    tag_id: Output[str]
    path: Output[str]

    def __init__(self,
            name,
            workspace_path: Input[str],
            tag_name: Input[str],
            tracking_id: Input[str],
            firing_trigger_id: Input[List[str]], opts=None):
        full_args = {
            "tag_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            "name": name,
            "workspace_path": workspace_path,
            "tag_name": tag_name,
            "tracking_id": tracking_id,
            "firing_trigger_id": firing_trigger_id,
        }
        super().__init__(GAPageviewTagProvider(), name, full_args, opts)
