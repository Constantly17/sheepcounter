<?php
session_start();


echo "<pre>";
echo "REQUEST_URI: " . $_SERVER['REQUEST_URI'] . "\n";
echo "SCRIPT_NAME: " . $_SERVER['SCRIPT_NAME'] . "\n";
echo "PHP_SELF: " . $_SERVER['PHP_SELF'] . "\n";
print_r($_GET);

// Получим путь после phpinfo.php
$uri = $_SERVER['REQUEST_URI'];
$script = $_SERVER['SCRIPT_NAME'];
$path = strtok(substr($uri, strlen($script)), '?'); // обрезаем query string
$segments = array_values(array_filter(explode('/', $path)));

print_r($segments);


echo '<h1>SESSION INFO</h1>';
echo '<hr>';
echo '<table>';
foreach ($_SESSION as $k => $v) {
	$tr = '<tr>';	
	$tr .= '<td>'.'$_SESSION['.$k.']'.'</td>'.'<td>'.$v.'</td>';
	$tr .= '<tr>';
	echo $tr;
}

echo '</table>';
echo '<h1>$_SERVER ARRAY INFO</h1>';
echo '<hr>';
echo '<table>';
foreach ($_SERVER as $k => $v) {
	$tr = '<tr>';
	$tr .= '<td>'.'$_SERVER['.$k.']'.'</td>'.'<td>'.$v.'</td>';
	$tr .= '<tr>';
	echo $tr;
}

echo '</table>';

phpinfo();




?>