from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.publish_provider import \
    PublishProvider

from ..service import get_key_file_location
from .tag_provider import TagProvider


class Publish(Resource):
    """
    This resource publishes a GTM workspace.  It does this by first creating a Container Version
    from the workspace, and then publishing that version.

    See https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/workspaces/create_version
    and https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/versions/publish
    for more information.

    IMPORTANT: Due to the way GTM works, this resource should be used with care.
    When a Container Version is created, GTM deletes the original workspace.  This can cause Pulumi
    problems if you try to add new workspace resources after publishing, since the workspace ID
    in Pulumi's state will no longer exist.
    
    In addition, publishing a workspace *may* create a replacement workspace if there would be no
    workspaces left, and if so this workspace is UNTRACKED by Pulumi.
    
    Finally, versions cannot not be unpublished, so deletion of this resource has no effect.
    """
    container_version_id: Output[str]
    container_version_path: Output[str]

    def __init__(self, name, workspace_path, opts=None):
        full_args = {
            "key_location": get_key_file_location(),
            "workspace_path": workspace_path,
            "container_version_id": None,
            "container_version_path": None
        }
        super().__init__(PublishProvider(), name, full_args, opts)
