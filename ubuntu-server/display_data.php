<?php
// Database configuration
$servername = "172.20.241.50";  // Replace with the correct IP address if necessary
$username = "remote_user";       // Your MySQL username (e.g., root or another user)
$password = "your_password";     // Your MySQL password
$dbname = "ble_data";            // The name of your database

// Create a connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to get all records from the "sensor_values" table
$sql = "SELECT * FROM sensor_values";
$result = $conn->query($sql);

// Check if we have records
if ($result->num_rows > 0) {
    // Start an HTML table to display the data
    echo "<table border='1'>
            <tr>
                <th>ID</th>
                <th>X Value</th>
                <th>Y Value</th>
                <th>Z Value</th>
                <th>Position</th>
                <th>Timestamp</th>
            </tr>";

    // Output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . $row["id"] . "</td>
                <td>" . $row["x_value"] . "</td>
                <td>" . $row["y_value"] . "</td>
                <td>" . $row["z_value"] . "</td>
                <td>" . $row["pos_value"] . "</td>
                <td>" . $row["timestamp"] . "</td>
              </tr>";
    }

    echo "</table>";
} else {
    echo "0 results found.";
}

// Close the connection
$conn->close();
?>

