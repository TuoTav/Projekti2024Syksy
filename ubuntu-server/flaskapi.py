from flask import Flask, jsonify
import MySQLdb  # Import MySQLdb (mysqlclient)

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    connection = MySQLdb.connect(
        host="172.20.241.50",  # Your MySQL server IP
        user="remote_user",     # MySQL username
        passwd="your_password",  # MySQL password
        db="ble_data"            # Database name
    )
    return connection

@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM sensor_values"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    result = []
    column_names = [i[0] for i in cursor.description]
    for row in rows:
        result.append(dict(zip(column_names, row)))

    # Close connection
    cursor.close()
    connection.close()

    # Return data as JSON
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Expose the API on port 5000

