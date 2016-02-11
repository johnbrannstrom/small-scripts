<?php
    $ip = $_GET["ip"];
    $mac = $_GET["mac"];
    exec("wakeonlan -i $ip $mac");
?>
