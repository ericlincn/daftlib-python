# This code defines a custom SQLAlchemy extension called FlaskSQLAlchemy. 
# It includes a context manager called auto_commit that provides a convenient way to 
# perform auto-commit transactions with the SQLAlchemy session.

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
    def auto_commit(self) -> None:
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    
    def has_table(self, table_name:str) -> bool:
        inspect = sa.inspect(self.engine)
        return inspect.has_table(table_name)
    
    def create_table(self, model:sa.schema.Table) -> None:
        model.metadata.create_all(self.engine)
