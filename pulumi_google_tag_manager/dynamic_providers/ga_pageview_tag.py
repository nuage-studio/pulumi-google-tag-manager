from pulumi.dynamic import Resource
from pulumi import Input, Output
from .ga_pageview_tag_provider import GAPageviewTagProvider
from ..service import get_key_file_location


class GaPageviewTagArgs(object):
    workspace_path: Input[str]
    tag_name: Input[str]
    tracking_id: Input[str]

    def __init__(self, workspace_path, tag_name, tracking_id):
        self.workspace_path = workspace_path
        self.tag_name = tag_name
        self.tracking_id = tracking_id


class GAPageviewTag(Resource):
    """
    Represents a Google Analytics UA tag in GTM which tracks page views.
    """
    tag_id: Output[str]
    path: Output[str]

    def __init__(self, name, args: GaPageviewTagArgs, opts=None):
        full_args = {
            "tag_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            **vars(args),
        }
        super().__init__(GAPageviewTagProvider(), name, full_args, opts)
