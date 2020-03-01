from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
from pulumi import Input, Output
from .web_property_provider import WebPropertyProvider


class WebPropertyArgs(object):
    account_id: Input[str]
    site_name: Input[str]
    site_url: Input[str]

    def __init__(
        self, account_id, site_name, site_url,
    ):
        self.account_id = account_id
        self.site_name = site_url


class WebProperty(Resource):
    tracking_id: Output[str]

    def __init__(self, name, args: WebPropertyArgs, opts=None):
        full_args = {**vars(args)}
        super().__init__(WebPropertyProvider(), name, full_args, opts)
