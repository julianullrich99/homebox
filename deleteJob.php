<?php
$data = $_POST["id"];

// phpinfo();

error_reporting(E_ALL);
//

$string = '{"type":"schedule","action":"deleteJob", "data": '.$data.'}';

echo $string;

echo CommunicateWithRobot($string);

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
        return "success";
        // Get the response from the server - our current telemetry
        // $resultLength = socket_read($socket);
        // if (strlen($resultLength) == 0) {
        //     return "Error: emptyness passed back from server";
        // }
        // else {
        //     $Telemetry = socket_read($socket, ord($resultLength));
        // }
        // $Telemetry = socket_read($socket,100000000);
        // socket_close($socket);
        // return $Telemetry;
    }


?>
