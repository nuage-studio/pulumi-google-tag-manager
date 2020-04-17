from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class DataLayerVariableProvider(ResourceProvider):
    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        variable_body = self._get_variable_body(props)
        
        variable = (
            service.accounts()
            .containers()
            .workspaces()
            .variables()
            .create(parent=props["workspace_path"], body=variable_body)
            .execute()
        )

        return CreateResult(id_=props["workspace_path"], outs={
            **props,
            **variable,
            "variable_id": variable["variableId"]
        })

    def update(self, id, _olds, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        variable_body = self._get_variable_body(props)
        variable = (
            service.accounts()
            .containers()
            .workspaces()
            .variables()
            .update(path=_olds["path"], body=variable_body)
            .execute()
        )

        return UpdateResult(outs={
            **props,
            **variable,
            "variable_id": variable["variableId"]
        })

    def delete(self, id, props):
        service = get_service("tagmanager", "v1", SCOPES, props['key_location'])
        service.accounts().containers().variables().delete(
            accountId=props["accountId"],
            containerId=props["containerId"],
            variableId=props["variableId"],
        )


    def _get_variable_body(self, props):
        return {
            "name": props["variable_name"],
            "type": "v",
            "parameter": [
                {
                    "type": "integer",
                    "key": "dataLayerVersion",
                    "value": "2"
                },
                {
                    "type": "boolean",
                    "key": "setDefaultValue",
                    "value": "false"
                },
                {
                    "type": "template",
                    "key": "name",
                    "value": props["variable_name"]
                }
            ],
        }
