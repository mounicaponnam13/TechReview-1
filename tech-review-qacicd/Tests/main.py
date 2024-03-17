import psycopg2

# Establish a connection to the PostgreSQL database
class databaseCheck:
    def create_connection(self):
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="db",
                port="5432",
                database="test_db"
            )
            print("Connection to PostgreSQL successful")
            self.connection = connection
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return None

    def createTable(self):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS testing_table (Name VARCHAR(255),Age NUMERIC,Salary FLOAT)")
            self.connection.commit()

    def insertDataInEmployeeTable(self, name, age, salary):
        if self.connection is not None:
            cursor = self.connection.cursor()
            sql = f'''INSERT INTO testing_table (Name, Age, Salary) VALUES ('{name}', {age}, {salary})'''
            try:
                # Execute the SQL command for each set of data
                cursor.execute(sql)
                # Commit your changes to the database
                self.connection.commit()
                print("Data inserted successfully")
                return True

            except Exception as e:
                # Rollback in case there is any error
                self.connection.rollback()
                print("Error:", e)
                return False

    def get_data_from_db(self):
        if self.connection is not None:
            try:
                # Create a cursor object
                cur = self.connection.cursor()
                # Define your SQL statement to select all rows from the table
                select_query = "SELECT * FROM testing_table"
                # Execute the SQL statement
                cur.execute(select_query)
                # Fetch all rows from the result set
                rows = cur.fetchall()
                # Print or process the fetched rows
                data=[]
                for row in rows:
                    data.append(row)
                # Close the cursor and connection
                cur.close()
                return data

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while fetching data from PostgreSQL:", error)
                return None

    def delete_data_from_db(self, name):
        if self.connection is not None:
            try:
                # Create a cursor object
                cur = self.connection.cursor()
                select_query = f"DELETE FROM testing_table WHERE name = '{name}'"
                cur.execute(select_query)
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while fetching data from PostgreSQL:", error)

    def get_count_of_rows(self):
        if self.connection is not None:
            try:
                # Create a cursor object
                cur = self.connection.cursor()
                # Define your SQL statement to select all rows from the table
                select_query = "SELECT * FROM testing_table"
                cur.execute(select_query)
                # Fetch all rows from the result set
                rows = cur.fetchall()
                # Print or process the fetched rows
                return len(rows)

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while fetching data from PostgreSQL:", error)
                return None

    def update_data_in_db(self, initial_name, final_name):
        if self.connection is not None:
            try:
                # Create a cursor object
                cur = self.connection.cursor()
                select_query = f"UPDATE testing_table SET name='{final_name}' WHERE name = '{initial_name}'"
                cur.execute(select_query)
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while updating data in PostgreSQL:", error)

    # Example usage:
    # if __name__ == '__main__':
    #     connection = create_connection()
    #     if connection is not None:
    #         # You can now execute SQL queries using this connection
    #         cursor = connection.cursor()
    #         cursor.execute("SELECT version();")
    #         record = cursor.fetchone()
    #         print("You are connected to - ", record)
    #         # Close the cursor and connection
    #         cursor.close()
    #         connection.close()
    #         print("PostgreSQL connection is closed")
