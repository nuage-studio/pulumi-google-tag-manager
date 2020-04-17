from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class PageviewTriggerProvider(ResourceProvider):
    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        trigger_body = self._get_trigger_body(props)
        
        trigger = (
            service.accounts()
            .containers()
            .workspaces()
            .triggers()
            .create(parent=props["workspace_path"], body=trigger_body)
            .execute()
        )

        return CreateResult(id_=props["workspace_path"], outs={
            **props,
            **trigger,
            "trigger_id": trigger["triggerId"]
        })

    def update(self, id, _olds, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        trigger_body = self._get_trigger_body(props)
        trigger = (
            service.accounts()
            .containers()
            .workspaces()
            .triggers()
            .update(path=_olds["path"], body=trigger_body)
            .execute()
        )

        return UpdateResult(outs={
            **props,
            **trigger,
            "trigger_id": trigger["triggerId"]
        })

    def delete(self, id, props):
        service = get_service("tagmanager", "v1", SCOPES, props['key_location'])
        service.accounts().containers().triggers().delete(
            accountId=props["accountId"],
            containerId=props["containerId"],
            triggerId=props["triggerId"],
        )


    def _get_trigger_body(self, props):
        return {
            "name": props["trigger_name"],
            "type": "pageview"
        }
