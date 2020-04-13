from typing import List

from pulumi import Input, Output
from pulumi.dynamic import Resource
from .custom_html_tag_provider import CustomHtmlTagProvider

from ..service import get_key_file_location


class CustomHtmlTagArgs(object):
    """
    Describes a GTM Custom HTML Tag.  See https://support.google.com/tagmanager/answer/6107167?hl=en#CustomHTML
    """

    workspace_path: Input[str]
    """
    GTM Workspace's API relative path. Example: accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}
    """

    tag_name: Input[str]
    """
    The name of the tag in GTM
    """

    html: Input[str]
    """
    The HTML content which will be rendered when the tag is triggered
    """

    support_document_write: Input[bool]
    """
    Whether or not `document.write()` is supported in the tag's HTML
    """

    firing_trigger_id: Input[List[str]]
    """
    A list of trigger IDs which cause this tag to fire
    """

    def __init__(self,
            workspace_path,
            tag_name,
            html,
            support_document_write = None,
            firing_trigger_id = []
            ):
        self.workspace_path = workspace_path
        self.tag_name = tag_name
        self.html = html
        self.support_document_write = support_document_write
        self.firing_trigger_id = firing_trigger_id


class CustomHtmlTag(Resource):
    tag_id: Output[str]
    path: Output[str]

    def __init__(self, name, args: CustomHtmlTagArgs, opts=None):
        full_args = {
            "tag_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            **vars(args),
        }
        super().__init__(CustomHtmlTagProvider(), name, full_args, opts)
