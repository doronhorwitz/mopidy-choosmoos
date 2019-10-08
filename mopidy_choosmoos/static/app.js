(function($) {
    'use strict';

    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/startsWith#Polyfill
    if (!String.prototype.startsWith) {
        Object.defineProperty(String.prototype, 'startsWith', {
            value: function(search, rawPos) {
                var pos = rawPos > 0 ? rawPos|0 : 0;
                return this.substring(pos, pos + search.length) === search;
            }
        });
    }

    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith#Polyfill
    if (!String.prototype.endsWith) {
        String.prototype.endsWith = function(search, this_len) {
            if (this_len === undefined || this_len > this.length) {
                this_len = this.length;
            }
            return this.substring(this_len - search.length, this_len) === search;
        };
    }

    var ws,
        $playlistTable,
        $websocketStatus,
        rowTemplateFunc;

    function getCurrentHost() {
        return (typeof document !== 'undefined' &&  document.location.host) || 'localhost';
    }

    function getCurrentProtocol() {
        return (typeof document !== 'undefined' && document.location.protocol === 'https:') ? 'https' : 'http';
    }

    function cacheJqueryObjects() {
        $playlistTable = $('#playlist-table tbody');
        $websocketStatus = $('#websocket-status');
        rowTemplateFunc = doT.template($('#row-template').text());
    }

    function getAllPlaylists() {
        return $.get(getCurrentProtocol() + "://" + getCurrentHost() + '/choosmoos/http/all-playlists').then(function(data){
            $.each(data.playlists, function(_, playlist) {
                $playlistTable.append(rowTemplateFunc({
                    playlistName: playlist.name,
                    tagUuid: playlist.tag_uuid,
                    playlistUri: playlist.playlist_uri
                }));
            });
            $playlistTable.find('button').on('click', function(e){
                e.preventDefault();
                var $button = $(this),
                    playlistUri = $button.closest('tr').attr('data-playlist-uri')

                $button.text("Requested...");
                wsSend('assign_tag_to_playlist', {
                    'playlist_uri': playlistUri
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
            } else if (action.startsWith('tag_')) {
                var buttonText = null,
                    playlistUri = data['params']['playlist_uri'],
                    tagUuid = data['params']['tag_uuid'],
                    $playlistRow = $playlistTable.find('tr[data-playlist-uri="' + playlistUri + '"]');

                if (action.endsWith('write_ready')) {
                    buttonText = "Ready to assign tag...";
                } else if (action.endsWith('assign_success')) {
                    buttonText = "Assign";
                    var $oldPlaylistRow = $playlistTable.find('tr[data-tag-uuid="' + tagUuid + '"]'),
                        oldPlaylistUri = $oldPlaylistRow.attr('data-playlist-uri');

                    if (oldPlaylistUri !== playlistUri) {
                        $oldPlaylistRow.removeAttr('data-tag-uuid');
                        $oldPlaylistRow.find('.tag-uuid').text('(not assigned)');
                        $playlistRow.attr('data-tag-uuid', tagUuid);
                        $playlistRow.find('.tag-uuid').text(tagUuid);
                    }
                } else if (action.endsWith('assign_failure')) {
                    buttonText = "Tag assign failed";
                }

                if (buttonText) {
                    $playlistRow.find('button').text(buttonText)

                }
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
