# This code defines a custom SQLAlchemy extension called FlaskSQLAlchemy. 
# It includes a context manager called auto_commit that provides a convenient way to 
# perform auto-commit transactions with the SQLAlchemy session.

# A context manager is a Python feature that allows you to manage resources and 
# setup/teardown actions in a with-statement block. It defines methods __enter__() and __exit__() 
# that are executed when entering and exiting the with-block, respectively.

# In this case, @contextmanager decorator is used from the contextlib module to create 
# a context manager for FlaskSQLAlchemy. The auto_commit context manager wraps 
# a block of code where you can perform database operations, 
# and it will automatically commit the changes if no exceptions are raised. 
# If an exception occurs within the block, it will perform a rollback on the session.

# Here's how you can use it:

# app = Flask(__name__)
# db = FlaskSQLAlchemy(app)
# @app.route('/example')
# def example():
#     with db.auto_commit():
#         # Perform database operations here, For example, adding a new record:
#         new_record = YourModel(name='example', value=123)
#         db.session.add(new_record)
#     # The changes will be automatically committed at the end of the with-block if no exceptions occurred.
#     return 'Transaction completed!'

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

class FlaskSQLAlchemy(SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    
    def has_table(self, table_name:str) -> bool:
        inspect = sa.inspect(self.engine)
        return inspect.has_table(table_name)