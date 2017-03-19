<?php
	session_start();
	require "connectserver.php";
	$username = $_SESSION["username"];
	if (!isset($_SESSION["username"])) {
		header("location:index.php");
	}
	// echo $username;
	// $sql = "SELECT myname FROM users WHERE username = '$username'";
	// $res = mysql_query($sql); //run the database
	// $arr = mysql_fetch_assoc($res); 
	// $myname = $arr['myname'];
	// echo $myname;
	$myname = $_SESSION["myname"];
	//find the authors from the authors database.
	$sql = "SELECT * FROM authors WHERE author = '$myname' ORDER BY pid";
	$res = mysql_query($sql); //get the query result from database
	$num = mysql_num_rows($res);
?>


<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>personalpaper</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<!-- <link rel="stylesheet" href="style.css"> -->
</head>


<body>

<div class="container">
<!-- below is to set the navbar: Home and Favorite papers in the Cart -->
<nav class="navbar navbar-toggleable-md navbar-light">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="index.php">References</a>
    </div>
    <!-- Home and Cart -->
    <ul class="nav navbar-nav navbar-right">
   	  <li><a href="userpage.php" class="btn btn-lg" ><span class="glyphicon glyphicon-user"></span> Hi,<?php echo $myname."!"?></a></li>
      <li><a href="favorite.php" class="btn btn-lg"><span class="glyphicon glyphicon-shopping-cart"></span> Cart</a></li>

      <li><a href="index.php?logout=true" class="btn btn-lg" ><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
    </ul>
  </div>
</nav>


<?php
if ($num > 0){
		echo "<br><br>";
		echo "<h4>There are " . mysql_num_rows($res) . " paper(s) you have published.</h4>";
	?>
	<table class="table table-hover">
		<thead>
		  <tr class="info">
		    <th>Title</th>
		    <th>Venue</th>
		    <th>Year</th>
		    <!-- <th>Delete</th> -->
		  </tr>
		</thead>
		<!-- </table> -->
	<?php
		while($data = mysql_fetch_assoc($res)){
			$pid = $data['pid'];
			$rst = "SELECT * FROM papers WHERE pid = '$pid' ORDER BY pid";
			$sql=mysql_query($rst);
			// echo $rst;
			$paper = mysql_fetch_assoc($sql); //get the papars with title and year,venue
	?>
		<tbody>
		<tr>
		    <td><?php echo "<h4> {$paper['title']}<h4>";?></td>
		    <td><?php echo "<h4> {$paper['venue']}<h4>";?></td>
		    <td><?php echo "<h4> {$paper['year']}<h4>";?></td>
		</tr>
		</tbody>
	<?php
		}
	} else{
		echo "<h3><center>You have not published paper yet.</center></h3>";
	}
	?>
</table>

</div>

</body>

</html>