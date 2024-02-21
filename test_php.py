<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Execute Python Script</title>
</head>
<body>

<h2>Click the button to generate the table:</h2>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
    <input type="submit" name="generate_table" value="Generate Table">
</form>

<?php
// Function to generate table
function generate_table() {
    // Execute the Python script and capture its output
    $output = exec("python script.py");

    // Split the output into rows
    $rows = explode("\n", $output);

    // Start building the HTML table
    echo "<table border='1'>";

    // Loop through each row and create table rows
    foreach ($rows as $row) {
        // Split each row into columns
        $columns = explode(",", $row);
        
        // Create table row
        echo "<tr>";
        
        // Loop through columns and create table cells
        foreach ($columns as $column) {
            echo "<td>" . $column . "</td>";
        }
        
        // Close table row
        echo "</tr>";
    }

    // Close HTML table
    echo "</table>";
}

// Check if the button is clicked
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['generate_table'])) {
    // Call the function to generate the table
    generate_table();
}
?>

</body>
</html>