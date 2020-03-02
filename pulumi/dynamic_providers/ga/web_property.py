from pulumi.dynamic import Resource
from pulumi import Input, Output
from .web_property_provider import WebPropertyProvider
from ..service import get_key_file_location


class WebPropertyArgs(object):
    account_id: Input[str]
    site_name: Input[str]
    site_url: Input[str]

    def __init__(
        self, account_id, site_name, site_url,
    ):
        self.account_id = account_id
        self.site_name = site_name
        self.site_url = site_url


class WebProperty(Resource):
    tracking_id: Output[str]

    def __init__(self, name, args: WebPropertyArgs, opts=None):
        full_args = {
            "tracking_id": None,
            "key_location": get_key_file_location(),
            **vars(args),
        }
        super().__init__(WebPropertyProvider(), name, full_args, opts)
