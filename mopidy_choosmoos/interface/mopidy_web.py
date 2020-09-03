class MopidyWeb:
    def __init__(self, websocket_handler):
        self._websocket_handler = websocket_handler

    def send_tag_write_ready(self, playlist_uri):
        self._websocket_handler.send_json_msg(
            "tag_write_ready", {"playlist_uri": playlist_uri}
        )

    def send_tag_assign_success(self, playlist_uri, tag_uuid):
        self._websocket_handler.send_json_msg(
            "tag_assign_success",
            {
                "playlist_uri": playlist_uri,
                "tag_uuid": tag_uuid,
            },
        )

    def send_tag_assign_failure(self, playlist_uri):
        self._websocket_handler.send_json_msg(
            "tag_assign_failure", {"playlist_uri": playlist_uri}
        )
