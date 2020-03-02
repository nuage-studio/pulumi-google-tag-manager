from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service

SCOPES = ["https://www.googleapis.com/auth/analytics.edit"]


class WebPropertyProvider(ResourceProvider):
    def create(self, props):
        service = get_service("analytics", "v3", SCOPES, props["key_location"])

        properties = (
            service.management()
            .webproperties()
            .list(accountId=props["account_id"], fields="items")
            .execute()
        )

        if properties.get("items"):
            # check if property already exists then simply return tracking code from property
            for p in properties.get("items"):
                if props["site_name"] == p.get("name"):
                    return CreateResult(
                        id_=props["account_id"], outs={"tracking_id": p["id"], **props},
                    )
        web_property = (
            service.management()
            .webproperties()
            .insert(
                accountId=props["account_id"],
                fields="id",
                body={"websiteUrl": props["site_url"], "name": props["site_name"]},
            )
            .execute()
        )

        return CreateResult(
            id_=props["account_id"], outs={"tracking_id": web_property["id"], **props},
        )

    def update(self, id, _olds, props):
        service = get_service("analytics", "v3", SCOPES, props["key_location"])

        web_property = (
            service.management()
            .webproperties()
            .update(
                accountId=props["account_id"],
                webPropertyId=_olds["tracking_id"],
                body={"websiteUrl": props["site_url"], "name": props["site_url"]},
            )
            .execute()
        )

        return UpdateResult(outs={"tracking_id": web_property["id"], **props})
