(function($) {
    'use strict';

    var $playlistList;

    function getCurrentHost() {
        return (typeof document !== "undefined" &&  document.location.host) || "localhost";
    }

    function getCurrentProtocol() {
        return (typeof document !== "undefined" && document.location.protocol === "https:") ? 'https' : 'http';
    }

    function cacheJqueryObjects() {
        $playlistList = $('#playlist-list');
    }

    function getAllPlaylists() {
        $.get(getCurrentProtocol() + "://" + getCurrentHost() + "/choosmoos/http/all-playlists").done(function(data){
            console.log(data);
            $.each(data.playlists, function(_, playlist){
                console.log(playlist.id);
                $playlistList.append('<li>' + playlist.id + ': ' + playlist.name + ' - ' + (playlist.db_id || '(not assigned)') + '</li>');
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
