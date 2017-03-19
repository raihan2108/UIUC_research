<?php
	session_start();
	require "connectserver.php"; //connect server
	// mysql_select_db('hshao5_cs411');
	$flag = 0;
	if (isset($_POST['register'])) {
		// session_start();
		$username = mysql_real_escape_string($_POST['username']); //get the username
		$myname = mysql_real_escape_string($_POST['myname']); //get the real name of users
		$email = mysql_real_escape_string($_POST['email']);
		$password = mysql_real_escape_string($_POST['password']);
		$password2 = mysql_real_escape_string($_POST['password2']);
		$sql = "SELECT * FROM users WHERE username = '$username'";
		$rst = mysql_query($sql); //get the query result from database
		$count=mysql_num_rows($rst);
		
		if ($count >= 1){
			$flag = 1;
			// echo "<script>setTimeout(\"location.href = 'index.php';\",1500);</script>";
		}else{
			if (($password2 == $password)&&!empty($password)&&!empty($email)&&!empty($myname)&&!empty($username)){
				//create users
				$password = md5($password);  //security passwor
				//database attributes: users(username,myname,email,password)
				$sql = "INSERT INTO users(username,myname,email,password) VALUES('$username','$myname','$email','$password')";
				mysql_query($sql);
				echo "<h4>You are registered now, please log in.<h4>";
				echo "<script>setTimeout(\"location.href = 'index.php';\",1200);</script>";
			}elseif(empty($username)){
				$flag = 2;
			}elseif (empty($myname)) {
				$flag =3;
			}elseif (empty($email)) {
				$flag = 4;
			}else{
				$flag = 5; //password is empty
			}

		}
	}

?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>register user</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<!-- <link rel="stylesheet" href="style.css"> -->
</head>

<body style="background-color: white">
<form method="post" action="register.php">
	<div class="container">
	<a href="register.php"><h3 class="text-center" style="color: blue">Please Register Your Personal Information</h3></a>
	<p>
	<?php
		if (isset($_POST['register'])){
			if ($flag == 1) {
				echo '<center><h4> <font color="red">Username has been registered!!!</font><h4></center>';
			}
			elseif($flag == 2){
				echo '<center><h4><font color="red">please input your UserID!!</font></h4></center>';
			}elseif ($flag==3) {
				echo '<center><h4><font color="red">please input your real name!!</font></h4></center>';
			}elseif ($flag==4) {
				echo '<center><h4><font color="red">please input your email!!</font></h4></center>';
			}else{
				echo '<center><h4><font color="red">please input your password!!</font></h4></center>';
			}
		}
	?>
	</p>
	<div class="col-md-4 col-md-offset-4">
		<div class="form-group">
    		<label for="uid"><h4>UserID:</h4></label>
    		<input type="text" class="form-control" name="username" placeholder="username">
		</div>
		<div class="form-group">
    		<label for="name"><h4>RealName:</h4></label>
    		<input type="text" class="form-control " name="myname" placeholder="first last name">
		</div>
		<div class="form-group">
    		<label for="eml"><h4>Email:</h4></label>
    		<input type="email" class="form-control" name="email" placeholder="email">
		</div>
		<div class="form-group">
			<label for="pwd"><h4>Password:</h4></label>
			<input type="password" class="form-control " name="password" placeholder="password">
		</div>
		<div class="form-group">
			<label for="pwd"><h4>Password Confirmation:</h4></label>
			<input type="password" class="form-control" name="password2" placeholder="password again">
		</div>
		<button type="submit" class="btn btn-primary" name="register">Register</button>
		<a href="index.php"><button type="button" class="btn btn-secondary">Home</button></a>
	</div>
	</div>

</form>

</body>



</html>