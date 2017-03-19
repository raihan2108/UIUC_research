<?php
	//connect to the database
	$db = mysql_connect("localhost", "root", "shj1987");
	mysql_select_db("cs411"); //very important to query data
	if (!$db) {
		die('Could not connect: ' . mysql_error());
	}
?>