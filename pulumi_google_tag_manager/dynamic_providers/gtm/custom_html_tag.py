from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.gtm.custom_html_tag_provider import \
    CustomHtmlTagProvider

from ..service import get_key_file_location
from .tag_provider import TagProvider


class CustomHtmlTagArgs(object):
    workspace_path: Input[str]
    tag_name: Input[str]
    html: Input[str]
    supportDocumentWrite: Input[bool]

    def __init__(self, workspace_path, tag_name, html, supportDocumentWrite = None):
        self.workspace_path = workspace_path
        self.tag_name = tag_name
        self.html = html
        self.supportDocumentWrite = supportDocumentWrite


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
