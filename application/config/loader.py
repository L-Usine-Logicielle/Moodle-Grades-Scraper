from os import environ

def load_variables(var : str):
    if var in environ:
        variable = environ[var]
        return variable
 
    raise RuntimeError(f'Please, define var : {var}')