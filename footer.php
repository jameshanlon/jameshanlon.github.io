</div> <!-- main -->
</div> <!-- outer -->

<?php
function get_page_mod_time() {
    $incls = get_included_files();
    $incls = array_filter($incls, "is_file");
    $mod_times = array_map('filemtime', $incls);
    $mod_time = max($mod_times);
    return $mod_time;
}
?>

<div id="footer">
You can contact me through mail@thisdomain.

<?php
echo "Last modified: " . date ("F d Y", get_page_mod_time());
?>
</div>

</body>
</html>

