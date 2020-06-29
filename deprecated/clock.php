<?php
$mode = $_GET["brightness"];
echo $mode;
CommunicateWithRobot('{"type":"mqtt","action":"clockBright","data": "'.$mode.'"}');

function CommunicateWithRobot($Commands) {
        // Create a TCP/IP socket.
        $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($socket === false) {
            return "Error: socket_create() failed: reason: " .
                socket_strerror(socket_last_error());
        }

        // Connect to the server running on the 'bot
        $result = socket_connect($socket, '127.0.0.1', '44148');
        if ($result === false) {
            return "Error: socket_connect() failed.\nReason: ($result) " .
                socket_strerror(socket_last_error($socket));
        }
        // Write two transmission, one of the size of the package,
        // and the second the package itself
        //socket_write($socket, chr(strlen($Commands)), 1);
        socket_write($socket, $Commands, strlen($Commands));

        // Get the response from the server - our current telemetry
        // $resultLength = socket_read($socket, 1);
        // if (strlen($resultLength) == 0) {
        //     return "Error: emptyness passed back from server";
        // }
        // else {
        //     $Telemetry = socket_read($socket, ord($resultLength));
        // }
        // socket_close($socket);
        // return $Telemetry;
    }


?>
