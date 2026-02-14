<?php
$salt = 'f789bbc328a3d1a3';

for($i=1424869663; $i < 1835970773; $i++ ){
    echo $i . '/' . 1835970773 . "\n";

    $hash = md5($salt . $i);
    if (preg_match('/^0e\d+$/', $hash)) {
        echo "FOUND: $i\n";
        echo "HASH: $hash\n";
        break;
    }
}
?>