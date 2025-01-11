<?php
$memcached = new Memcached();
$memcached->addServer('memcached', 11211);

// Test zapisu do Memcached
$testKey = 'test_key';
$testValue = 'PrestaShop Memcached Test';
$memcached->set($testKey, $testValue, 60);

// Test odczytu z Memcached
$result = $memcached->get($testKey);

if ($result === $testValue) {
    echo 'Memcached działa poprawnie: ' . $result;
} else {
    echo 'Błąd połączenia z Memcached.';
}
?>
