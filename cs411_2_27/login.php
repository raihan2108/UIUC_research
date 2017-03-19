<?php
	//connect to the database
	session_start();
	require "connectserver.php";
	$myusername = $_POST["username"]; //get the username
	$mypassword = $_POST["password"];
	$myusername = stripcslashes($myusername);
	$mypassword = stripcslashes($mypassword);
	$mypassword= md5($mypassword);
	// mysql_select_db('hshao5_cs411');
	if (isset($_POST["login"])) {
		// session_start();
		$sql = "SELECT * FROM users WHERE username = '$myusername' and password = '$mypassword'";
		$rst = mysql_query($sql); //get the query result from database
		$count=mysql_num_rows($rst);
		if ($count ==1){
			$_SESSION['username'] = $myusername;
			header("location:userpage.php"); //redirect to the homepage to log in
			// echo "<h3>logged in successfully.<h3>";
			// echo "<script>setTimeout(\"location.href = 'userpage.php';\",1500);</script>";
		}else{
			echo "<h3>Wrong user name or password, please input again.</h3>";
			echo "<script>setTimeout(\"location.href = 'index.php';\",1200);</script>";

		}

	}

?>