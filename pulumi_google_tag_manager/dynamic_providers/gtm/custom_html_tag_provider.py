from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class CustomHtmlTagProvider(ResourceProvider):
    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)
        tag = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .create(parent=props["workspace_path"], body=tag_body)
            .execute()
        )

        return CreateResult(id_=props["workspace_path"], outs={**props, **tag})

    def update(self, id, _olds, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)
        tag = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .update(path=_olds["path"], body=tag_body)
            .execute()
        )

        return UpdateResult(outs={**props, **tag})

    def delete(self, id, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        service.accounts().containers().workspaces().tags().delete(
            path=props["path"]
        ).execute()


    def _get_tag_body(self, props):
        
        params = [
            {
                "key": "html",
                "type": "template",
                "value": props["html"],
            }
        ]
        if props.get("supportDocumentWrite") is not None:
            params.append({
                "key": "supportDocumentWrite",
                "type": "boolean",
                "value": str(props["supportDocumentWrite"]).lower(),
            })

        tag_body = {
            "name": props["tag_name"],
            "type": "html",
            "parameter": params,
        }

        return tag_body