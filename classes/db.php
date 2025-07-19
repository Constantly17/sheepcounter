<?php


class Database {
    private $host = 'CONSTANTLY_PC';
    private $username = 'web_user';
    private $password = '48625';
    private $conn;

    public function __construct() {
       // $this->conn = new PDO('sqlsrv:server='.$this->host.',1433;TrustServerCertificate=true;', $this->username, $this->password);
		 $this->conn = new PDO('sqlsrv:server='.$this->host.',1433;', $this->username, $this->password);
        $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    public function query($query, $params = array()) {
		//var_dump($query);
        $result = $this->conn->prepare($query);
        if (!empty($params)) {
			//var_dump($result);
            $result->execute($params);
        } else {
            $result->execute();
        }
        return $result;
    }
}
?>
