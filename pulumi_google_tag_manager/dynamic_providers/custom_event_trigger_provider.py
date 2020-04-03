from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class CustomEventTriggerProvider(ResourceProvider):
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
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        service.accounts().containers().workspaces().triggers().delete(
            path=props["path"]
        ).execute()


    def _get_trigger_body(self, props):
        return {
            "name": props["trigger_name"],
            "type": "customEvent",
            "customEventFilter": [
                {
                    "type": "equals",
                    "parameter": [
                        {
                            "type": "template",
                            "key": "arg0",
                            "value": "{{_event}}"
                        },
                        {
                            "type": "template",
                            "key": "arg1",
                            "value": props["trigger_name"]
                        }
                    ]
                }
            ]
        }
