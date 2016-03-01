from tracker import consumers

channel_routing = {
    "websocket.connect": consumers.websocket_connect,
    "websocket.keepalive": consumers.websocket_keepalive,
    "websocket.disconnect": consumers.websocket_disconnect
}
