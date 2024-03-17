import unittest
from decimal import Decimal
from main import databaseCheck
from ContextStorage import contextStorage


class TestMyFunctions(unittest.TestCase):
    # Define test methods starting with the word "test"
    contextStorage = contextStorage()

    def test_db_connection(self):
        database_check = databaseCheck()
        connection = database_check.create_connection()
        contextStorage.database_check_local = database_check
        if connection is None:
            assert True == False, 'Unable to create connection with database'
        else:
            assert True

    def test_insert_in_db(self):
        data_to_update = ('Mounica', 20, 60000.50)
        contextStorage.database_check_local.delete_data_from_db(data_to_update[0])
        contextStorage.database_check_local.createTable()
        status = contextStorage.database_check_local.insertDataInEmployeeTable(data_to_update[0], data_to_update[1], data_to_update[2])
        assert status is True, 'Table insertion failed'
        assert contextStorage.database_check_local.get_count_of_rows() == 1, 'insertion dint worked'
        returned_data = contextStorage.database_check_local.get_data_from_db()[0]
        assert returned_data == data_to_update, 'data objects are not same which we insert'
        assert isinstance(returned_data, tuple), 'Data is not instance of tuple'
        assert isinstance(returned_data[1], Decimal), 'Age column is not in Decimal'
        assert isinstance(returned_data[2], float), 'Numeric value of salary is not in float'
        assert returned_data[1] == data_to_update[1], 'Age data of sql and what we inserted is not same'

    def test_update_row_functionality(self):
        previous_name = 'Mounica'
        updated_name = 'Testing'
        status = contextStorage.database_check_local.update_data_in_db(previous_name, updated_name)
        data = contextStorage.database_check_local.get_data_from_db()
        assert (data[0])[0] == updated_name, 'updation not working'
        

# This block allows the test script to be executed directly
if __name__ == '__main__':
    unittest.main()
