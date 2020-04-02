from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.gtm.data_layer_variable_provider import \
    DataLayerVariableProvider
from pulumi_google_tag_manager.dynamic_providers.service import \
    get_key_file_location


class DataLayerVariable(Resource):
    """
    Represents a data layer variable, which can be set using the `dataLayer`. 
    See https://support.google.com/tagmanager/answer/7683362?hl=en&ref_topic=9125128
    """
    path: Output[str]
    variable_id: Output[str]

    def __init__(self,
            name: Input[str],
            variable_name: Input[str],
            workspace_path: Input[str],
            opts=None):
        super().__init__(DataLayerVariableProvider(), name, {
            "variable_name": variable_name,
            "key_location": get_key_file_location(),
            "workspace_path": workspace_path,
            "path": None,
            "variable_id": None
        }, opts)
