<!-- search the papers and authors -->
<?php 
	session_start();
	require "connectserver.php"; //connect server;
	$username = $_SESSION["username"];
	if (!isset($_SESSION["username"])) {
		header("location:index.php");
	}
	//get the real name
	$sql = "SELECT myname FROM users WHERE username = '$username'";
	$res = mysql_query($sql); //run the database
	$arr = mysql_fetch_assoc($res); 
	$myname = $arr['myname'];
	$_SESSION["myname"] = $myname;
	//search
	$searchConf = $searchYear = $searchAuthor = $searchJournal = ""; //iniate
	$case = 0;
	$query = "";
	// echo "test: home";
	$flg = 0;
	// search papers with year, venue and author.
	if (isset($_POST['search'])){
		// echo "test: search";
		$searchYear = $_POST["year"];
		$searchJournal = $_POST["journal"]; //get the venue: journal name and conf names
		$searchConf = $_POST["conf"];
		$searchAuthor =$_POST["author"];
		//Sql table named as papers(year,author,venue, paper_id)
		//name of database: papers, authors, confs, journals.
		if (!empty($searchYear)){
			$results="SELECT * FROM papers WHERE year = '$searchYear' ORDER BY pid";
			$case = 1;
		} elseif (!empty($searchAuthor)) {
			$results="SELECT * FROM authors WHERE author = '$searchAuthor' ORDER BY pid";
			$case = 2;
		} elseif (!empty($searchConf)){
			$results="SELECT * FROM confs WHERE cname = '$searchConf' ORDER BY pid";
			$case = 3;
		} elseif (!empty($searchJournal)){
			$results="SELECT * FROM journals WHERE jname = '$searchJournal' ORDER BY pid";
			$case = 4;
		} else{
			header("location:userpage.php");
		}
		$res=mysql_query($results);
	} 
	else if ( isset($_REQUEST['username']) && isset($_REQUEST['pid']) ) {
		// echo "test: favorite";
		$uid = $_REQUEST['username'];
		$pid = $_REQUEST['pid'];
		$sql = "SELECT * FROM favorpaper WHERE pid = '$pid' and userid = '$uid'";
		$rsts = mysql_query($sql); //get the query result from database
		$count=mysql_num_rows($rsts);
		
		$case = $_REQUEST["case"]; //detemine search author or year or journal
		$results ="";

		if ($case == 1) {
			$searchYear = $_REQUEST["query"];
			// echo $case.": ".$searchYear;
			$results="SELECT * FROM papers WHERE year = '$searchYear' ORDER BY pid";
		} else if ($case == 2) {
			$searchAuthor = $_REQUEST["query"];
			// echo $case.": ".$searchAuthor;
			$results="SELECT * FROM authors WHERE author = '$searchAuthor' ORDER BY pid";
		} else if ($case == 3) {
			$searchConf = $_REQUEST["query"];
			// echo $case.": ".$searchConf;
			$results="SELECT * FROM confs WHERE cname = '$searchConf' ORDER BY pid";
		} else if ($case == 4) {
			$searchJournal = $_REQUEST["query"];
			// echo $case.": ".$searchJournal;
			$results="SELECT * FROM journals WHERE jname = '$searchJournal' ORDER BY pid";
		}

		$res = mysql_query($results);

		if ($count ==0){
			// echo $uid."- add -".$pid;
			// echo "<p>There are " . mysql_num_rows($res) . " result(s) available.</p>";
			echo '<a><span style="color:red">'.$uid .' add paper '. $pid.'</span></a>';
			$sql = "INSERT INTO favorpaper(pid,userid) VALUES('$pid','$uid')";
			mysql_query($sql);
		}else{
			// $flg =1;
			echo "add the same paper.";
		}

	}
	// echo "test: end if";
// session_destroy();
?>

<!DOCTYPE html>
<html>
<head>
	<title>userpage</title>
	<meta charset="utf-8">
	<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<body>
<!-- <h2><?php echo $username; ?>Welcome to your homepage.</h2> -->
<div class="container">
<!-- below is to set the navbar: Home and Favorite papers in the Cart -->
<nav class="navbar navbar-toggleable-md navbar-light">
  <div class="container-fluid">
    <div class="navbar-header">
     <a class="navbar-brand" href="index.php"> References</a>
    </div>
    <!-- Home and Cart -->
    <ul class="nav navbar-nav navbar-right">
    	<li><a href="personal.php" class="btn btn-lg" ><span class="glyphicon glyphicon-list-alt"></span> Publication</a></li>
   	  <li><a href="userpage.php" class="btn btn-lg" ><span class="glyphicon glyphicon-user"></span> Hi,<?php echo $myname."!"?></a></li>
   	  <?php
   	  	// $uid = $_REQUEST['username'];
		// $pid = $_REQUEST['pid'];
		$sql = "SELECT * FROM favorpaper WHERE userid = '$username'";
		$rescart = mysql_query($sql); //get the query result from database

   	  ?>
      <li><a href="favorite.php" class="btn btn-lg"><span class="glyphicon glyphicon-shopping-cart"></span> Cart (<?php echo mysql_num_rows($rescart);?>)</a></li>

      <li><a href="index.php?logout=true" class="btn btn-lg" ><span class="glyphicon glyphicon-log-out"></span>Logout</a></li>
    </ul>
  </div>
</nav>
<!-- <h2 class="text-center">Welcome to your homepage <?php echo $username ;?></h2><br><br> -->
<!-- search the author and venue and years -->
<form method="post" action="userpage.php">
    <div class="form-group">
      <div class="col-xs-4">
        <label for="ex1"><h4>Journal</h4></label>
        <input class="form-control input-lg" id="ex1" type="text" name="journal" placeholder="journal">
      </div>
      <div class="col-xs-2">
        <label for="ex1"><h4>Conference</h4></label>
        <input class="form-control input-lg" id="ex1" type="text" name="conf" placeholder="conference">
      </div>
      <div class="col-xs-2">
        <label for="ex2"><h4>Author</h4></label>
        <input class="form-control input-lg" id="ex2" type="text" name="author" placeholder="author">
      </div>
      <div class="col-xs-2">
        <label for="ex3"><h4>Year</h4></label>
        <input class="form-control input-lg" id="ex3" type="text" name="year" placeholder="year">
      </div>
      <div class="col-xs-2">
      	<h4><br></h4>
      	<button type="submit" class="btn btn-info" name="search">
	    <span class="glyphicon glyphicon-search"></span> Search</button>
      </div>
	    
    </div>
 </form>
</div>

<div class="container">
<?php
if ( isset($_POST['search']) || isset($_REQUEST['username']) ){
	// if ($flg == 1){
	// 	echo '<a text-center><span style="color:red">Oops,add the same paper.</span></a>';
	// }
	// echo "test: into result";
	if (mysql_num_rows($res)>0){
		echo "<br><br>";
		echo "<p>There are " . mysql_num_rows($res) . " result(s) available.</p>";
?>
<table class="table table-hover">
	<thead>
	  <tr class="info">
	    <th>Title</th>
	    <th>Venue</th>
	    <th>Year</th>
	    <th>Add</th>
	  </tr>
	</thead>
	<!-- </table> -->
<?php
	if ($case == 1 ) {
		$query = $searchYear;
	}
	else if ($case == 2 ) {
		$query = $searchAuthor;
	}
	else if ($case == 3 ) {
		$query = $searchConf;
	}
	else if ($case == 4 ) {
		$query = $searchJournal;
	}
	// echo "test: case";
	while($data=mysql_fetch_assoc($res)){
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
	    	<!-- $searchConf = $searchYear = $searchAuthor = $searchJournal -->

	    <td><h4>
	    	<?php
				$sql_check = "SELECT * FROM favorpaper WHERE userid = '$username' AND  pid = '$pid' ";
				$res_check = mysql_query($sql_check); //get the query result from database
				$check_length = mysql_num_rows($res_check);
				if ($check_length <= 0) {
	    	?>
			<!-- if not exist in database -->
	    	<a href='userpage.php?username=<?php echo $username; ?>&pid=<?php echo $pid; ?>&case=<?php echo $case; ?>&query=<?php echo $query; ?>'><span class="glyphicon glyphicon-plus" style="color:black"></span> 
	    	</a>
			<?php
				} else { 
			?>
			<!-- if  exist in database -->
			<span class="glyphicon glyphicon-heart" style="color:red"></span>
			<?php
				}
			?>
	    	</h4></td>

		<!--  <span class="glyphicon glyphicon-plus" style="color:red"></span>-->

<!-- 	    <td><h4><a href="userpage.php?username=<?php echo $username; ?>&pid=<?php echo $pid; ?>">
	    	<span class="glyphicon glyphicon-heart" style="color:red"></span>
	    	</a></h4></td>	 -->    	
	</tr>
	</tbody>
<?php	
	}
}else{
		echo "There is no result found.";
	}
  }
?>
</table>
</div>

</body>

</html>