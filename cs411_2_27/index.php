<?php
	session_start();
	require "connectserver.php"; //connect server;
	if (isset($_SESSION["username"])) {
		$username = $_SESSION["username"];
	}
	if (isset($_REQUEST['logout'])){
		$logout = $_REQUEST["logout"];
		if ($logout == "true"){
			echo "logout";
			unset($_SESSION["username"]); 
		}
	}
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Homepage</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<!-- <link rel="stylesheet" href="style.css"> -->
</head>

<body>
<form action="login.php" method="post">
	<div class="container">
	<h2 class="text-center"><strong>Welcome to the Academic Search System.</strong></h2>
	<br><br>
		<div class="col-md-4 col-md-offset-4">
		<div class="form-group">
    		<label for="uid"><h4>UserName:</h4></label>
    		<input type="text" class="form-control input-lg" name="username" placeholder="username">
		</div>
		
		<div class="form-group">
			<label for="pwd"><h4>Password:</h4></label>
			<input type="password" class="form-control input-lg" name="password" placeholder="password">
		</div>
		<button type="submit" class="btn btn-primary btn-lg" name="login">Login</button>
		<a href ="register.php" target="_blank"><button type= "button" class="btn btn-success btn-lg">Sign Up</button></a>
	</div>
	</div>


</form>

</body>

</html>