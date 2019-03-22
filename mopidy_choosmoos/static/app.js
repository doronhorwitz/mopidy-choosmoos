(function($) {
    'use strict';

    var ws,
        $playlistTable,
        $websocketStatus;

    function getCurrentHost() {
        return (typeof document !== 'undefined' &&  document.location.host) || 'localhost';
    }

    function getCurrentProtocol() {
        return (typeof document !== 'undefined' && document.location.protocol === 'https:') ? 'https' : 'http';
    }

    function cacheJqueryObjects() {
        $playlistTable = $('#playlist-table');
        $websocketStatus = $('#websocket-status');
    }

    function getAllPlaylists() {
        return $.get(getCurrentProtocol() + "://" + getCurrentHost() + '/choosmoos/http/all-playlists').then(function(data){
            $.each(data.playlists, function(_, playlist){
                $playlistTable.append('<tr><td>' + playlist.id + '</td><td>' + playlist.name + '</td><td>' + (playlist.db_id || '(not assigned)') + '</td><td><button data-id="' + playlist.id +'" disabled=\"disabled\">Assign</button></td></tr>');
            });
            $playlistTable.find('button').on('click', function(e){
                e.preventDefault();
                var $button = $(this),
                    playListId = $button.data('id');

                $button.text("Requested...");
                wsSend('assign_tag_to_playlist', {
                    'playlist_id': playListId
                });
            });
        });
    }

    function wsSend(action, params) {
        var dataToSend = {
            'action': action
        };
        if (params) {
            dataToSend['params'] = params;
        }
        ws.send(JSON.stringify(dataToSend));
    }

    function openWebSocket() {
        var protocol = getCurrentProtocol() === 'https' ? 'wss' : 'ws';
        ws = new WebSocket(protocol + "://" + getCurrentHost() + '/choosmoos/ws/');

        ws.onopen = function (event) {
            wsSend('open_websocket');
        };

        ws.onmessage = function (event) {
            var data = JSON.parse(event.data),
                action = data['action'];

            if (action === 'acknowledge_open_websocket') {
                $websocketStatus.text("Ready");
                $playlistTable.find("button").removeAttr("disabled");
            } else if (action === 'tag_write_ready') {
                var playlistId = data['params']['playlist_id'];
                $playlistTable.find('button[data-id="' + playlistId + '"]').text("Ready to assign tag...");
            } else if (action === 'tag_assign_success') {
                var playlistId = data['params']['playlist_id'];
                $playlistTable.find('button[data-id="' + playlistId + '"]').text("Tag assigned successfully");
            } else if (action === 'tag_assign_failure') {
                var playlistId = data['params']['playlist_id'];
                $playlistTable.find('button[data-id="' + playlistId + '"]').text("Tag assign failed");
            }
        }
    }

    $(function(){
        cacheJqueryObjects();
        getAllPlaylists().done(function(){
            openWebSocket();
        });
    });
}(jQuery));
