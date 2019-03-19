(function($) {
    'use strict';

    var $playlistTable;

    function getCurrentHost() {
        return (typeof document !== "undefined" &&  document.location.host) || "localhost";
    }

    function getCurrentProtocol() {
        return (typeof document !== "undefined" && document.location.protocol === "https:") ? 'https' : 'http';
    }

    function cacheJqueryObjects() {
        $playlistTable = $('#playlist-table');
    }

    function getAllPlaylists() {
        $.get(getCurrentProtocol() + "://" + getCurrentHost() + "/choosmoos/http/all-playlists").done(function(data){
            $.each(data.playlists, function(_, playlist){
                $playlistTable.append('<tr><td>' + playlist.id + '</td><td>' + playlist.name + '</td><td>' + (playlist.db_id || '(not assigned)') + '</td><td><button data-id="' + playlist.id +'">Assign</button></td></tr>');
            });
        });
    }

    function openWebSocket() {
        var protocol = getCurrentProtocol() === 'https' ? "wss" : "ws",
            ws = new WebSocket(protocol + "://" + getCurrentHost() + "/choosmoos/ws/");

        ws.onopen = function (event) {
            ws.send("Here's some text that the server is urgently awaiting!");
        };

        ws.onmessage = function (event) {
            console.log(event.data);
        }
    }

    $(function(){
        cacheJqueryObjects();
        openWebSocket();
        getAllPlaylists();
    });
}(jQuery));
