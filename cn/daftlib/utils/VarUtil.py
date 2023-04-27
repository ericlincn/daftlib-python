import getopt
import sys
import os
from typing import Any

class VarUtil:

    @staticmethod
    def getVars() -> list[str]:
        return sys.argv[1:]
    
    @staticmethod
    def getVarsBykeys(keys:list[str]) -> dict[str, Any]:
        try:
            opts, args = getopt.getopt(VarUtil.getVars(), '', [f'{key}=' for key in keys])
            kv_args = {}
            
            for opt, arg in opts:
                opt_name = opt[2:]
                if opt_name in keys:
                    kv_args[opt_name] = arg
            return kv_args

        except getopt.GetoptError as e:
            print(f"Error: {e}")
            return {}
    
    @staticmethod
    def getVarByEnv(env_key:str, default:str = None) -> str:

        if env_key in os.environ and os.environ.get(env_key):
            return os.environ[env_key]
        elif default is not None:
            return default
        else:
            raise ValueError(
                f"Did not find {env_key}, please add an environment variable"
                f" `{env_key}` which contains it."
            )