<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>James Hanlon</title>
<link rel="stylesheet" href="style.css" type="text/css" />
<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/jquery.tablesorter.min.js"></script>
<script type="text/javascript" src="js/d3.min.js"></script>
<script>
  $(document).ready(function() { $("#processors").tablesorter({
    sortInitialOrder: "desc" }); }); 
</script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-19458374-1', 'auto');
  ga('send', 'pageview');
</script>
</head>
<body>
<div id="outer">
<div id="main">
<div id="links">
<? if (strpos($_SERVER['SCRIPT_NAME'], 'index.php') == false) { ?>
<li><a href="index.php">&laquo; home</a></li>
<? } ?>
</div>
