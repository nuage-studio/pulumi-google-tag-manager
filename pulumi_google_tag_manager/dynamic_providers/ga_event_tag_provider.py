from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class GAEventTagProvider(ResourceProvider):
    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        tag_body = self.get_tag_body(props)
        
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
        tag_body = self.get_tag_body(props)

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
        service = get_service("tagmanager", "v1", SCOPES, props['key_location'])
        service.accounts().containers().tags().delete(
            accountId=props["accountId"],
            containerId=props["containerId"],
            tagId=props["tagId"],
        )

    def get_tag_body(self, props):
        return {
            "name": props["tag_name"],
            "type": "ua",
            "parameter": [
                {
                    # Whether or not the tag is considered an interation for computing the
                    # bounce rate.  See https://support.google.com/analytics/answer/1033068#NonInteractionEvents
                    "type": "boolean",
                    "key": "nonInteraction",
                    "value": "false"
                },
                {
                    # GA tracking code should not come from a settings variable, but from
                    # the `trackingId` attribute below
                    "type": "boolean",
                    "key": "overrideGaSettings",
                    "value": "true"
                },
                {
                    # The value associated with the event
                    "type": "template",
                    "key": "eventValue",
                    "value": props["event_value"]
                },
                {
                    # The category to register the event against on GA
                    "type": "template",
                    "key": "eventCategory",
                    "value": props["event_category"]
                },
                {
                    # This is a GA event which is being triggered
                    "type": "template",
                    "key": "trackType",
                    "value": "TRACK_EVENT"
                },
                {
                    # The action with the event is registered against on GA
                    "type": "template",
                    "key": "eventAction",
                    "value": props["event_action"]
                },
                {
                    # The GA tracking ID
                    "type": "template",
                    "key": "trackingId",
                    "value": str(props["tracking_id"])
                }
            ],
            "firingTriggerId": props["firing_trigger_id"]
        }
