<? include "header.php"?>

<div class="column">

<h1>A list of general-purpose parallel processors</h1>

<p>This page provides a (continually updated) catalouge of past and present
general-purpose parallel processors, along with their main characteristics.</p>

</div>

<h2>Number of cores over time</h2>

<div class="plot"></div>
<script type="text/javascript" src="js/scatter.js"></script>

<h2>The dataset</h2>

<table id="processors" class="tablesorter">
<thead>
<?php
$align=array(
  0  => "left",   1  => "center", 2  => "left",   3  => "center",
  4  => "center", 5  => "center", 6  => "center", 7  => "center",
  8  => "center", 9  => "center", 10 => "center", 11 => "center",
  12 => "center", 13 => "center", 14 => "center", 15 => "center",
  16 => "center", 17 => "center", 18 => "center", 15 => "center",
);
$cols = array(0, 1, 2, 3, 4, 5, 9, 12, 13);
$row = 0;
if (($handle = fopen("processor-list/dataset.csv", "r")) !== FALSE) {
  while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
    $bg = ($row % 2 == 1 ? "tr1" : "tr2");
    echo "<tr class=\"$bg\">\n";
    $num = count($data);
    $col = 0;
    foreach ($data as $d) {
      if ($row == 0) echo "<th class=\"$align[$col]\">" . $d . "</th>\n";
      else           echo "<td class=\"$align[$col]\">" . $d . "</td>\n";
      $col++;
    }
    echo "</tr>\n";
    if ($row == 0)
      echo "</thead>\n<tbody>\n";
    $row++;
  }
  fclose($handle);
}
?>
</tbody>
</table>

<div class="column">

<h2>Notes</h2>

<p>Notation:

<ul>
<li>DM means distributed memory;</li>
<li>SM means shared memory.</li>
</ul>
</p>

<p>For the purposes of this list:<br>

<ul>

<li>the term "processor" is taken to mean a single package, containing one or more
  chips that perform a computational function;</li>

<li>the term "parallel" is taken to mean a replication of machinary to improve
  aggregate performance;</li>

<li>the listed processors are general purpose in the sense that they are not
specialised to perform a single task or a small set of similar tasks;</li>

<li>only processors that have a level of parallelism of 8 or greater are
  included;</li>

<li>multithreading is taken to be a mechanism for parallelism.</li>

</ul>
</p>

<p>Please contact me to supply any corrections or additions to the dataset.</p>

<h2>The dataset</h2>

<p>Download the <a href="http://github.com/jameshanlon/processor-list">
dataset</a> (GitHub).</p>

<h2>See also</h2>

<ul>
<li><a href="http://cpudb.stanford.edu/">CPU DB</a></li>
<li><a href="http://www.cpu-world.com/">CPU World</a></li>
</ul>

</div>

<? include "footer.php"?>
