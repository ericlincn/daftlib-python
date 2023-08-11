from typing import Any
from flask_sqlalchemy import SQLAlchemy

class RuntimeModel:

    __table_dict = {}

    @staticmethod
    def model(db:SQLAlchemy, table_name:str, dict:dict[str, Any]):
        ModelClass = RuntimeModel.__table_dict.get(table_name, None)
        if ModelClass is None:
            dict['__module__'] = __name__
            # dict['__name__'] = table_name
            dict['__tablename__'] = table_name

            class_name = table_name.capitalize()
            ModelClass = type(class_name, (db.Model, ), dict)
            RuntimeModel.__table_dict[table_name] = ModelClass
        
        cls = ModelClass()
        cls.tablename = table_name
        return cls