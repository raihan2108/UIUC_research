<?php
	session_start();
	require "connectserver.php";
	$uid = $_SESSION["username"];
	// echo $uid;

	if ( isset($_REQUEST['username']) && isset($_REQUEST['pid']) ) {
		// echo "test: favorite";
		$uid = $_REQUEST['username'];
		$pid = $_REQUEST['pid'];
		// delete
		// DELETE FROM `favorpaper` WHERE `favorpaper`.`id` = 5"?
		$sql = "DELETE FROM favorpaper WHERE pid = '$pid' AND userid = '$uid'";
		mysql_query($sql); //get the query result from database
		echo "Delete favorpaper: ".$uid." & ".$pid;
	}

	$sql = "SELECT * FROM favorpaper WHERE userid = '$uid' ORDER BY pid";
	$res = mysql_query($sql); //get the query result from database



?>


<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>paperlist</title>
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
   	  <li><a href="userpage.php" class="btn btn-lg" ><span class="glyphicon glyphicon-user"></span> Hi,<?php echo $uid."!"?></a></li>
      <li><a href="favorite.php" class="btn btn-lg"><span class="glyphicon glyphicon-shopping-cart"></span> Cart (<?php echo mysql_num_rows($res);?>)</a></li>

      <li><a href="index.php?logout=true" class="btn btn-lg" ><span class="glyphicon glyphicon-log-out"></span>Logout</a></li>
    </ul>
  </div>
</nav>
<?php
// echo "<h3>The search results is :</h3>";
if (mysql_num_rows($res) > 0){
	echo "<br><br>";
	echo "<p>There are " . mysql_num_rows($res) . " paper(s) you like.</p>";
?>
<table class="table table-hover">
	<thead>
	  <tr class="info">
	    <th>Title</th>
	    <th>Venue</th>
	    <th>Year</th>
	    <th>Delete</th>
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
	    <!-- button of like the paper? -->
	    <td><h4><a href="favorite.php?username=<?php echo $uid;?> &pid=<?php echo $pid;?>"><span class="glyphicon glyphicon-remove-circle" style="color:red"></span></a></h4></td>
	</tr>
	</tbody>
<?php
	}
} else {
	header("location:userpage.php");
}
?>
</table>

</div>

</body>

</html>