"""
Python 3.6+

conndb is a module that creates sqlalchemy
engine information strings by parsing a java 
properties file that stores database credentials.

example properties file:

    db_host=ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com
    db_user=username
    db_password=password
    db_port=5432
    db_name=database
    environment=PROD

Author: Liam Xiao
Contributor: Adam Turner <turner.adch@gmail.com>
"""


def parse_props(props_path: str) -> dict:
    """Parses information needed to connect to db.

    Args:
        props_path: path to Java properties file.
    """
    print("Parsing db properties...")
    props = open(props_path).read().split("\n")
    delim = "="
    props = {kv.split(delim)[0]: kv.split(delim)[1] for kv in props if len(kv) >= 3}
    print("  > Property keys:", props.keys())
    return props


def get_engine_info(props_path: str) -> str:
    """Helps create sqlalchemy engines.

    Args:
        props_path: path to Java properties file
    """
    props = parse_props(props_path)
    engine_info = "{flavor}://{user}:{password}@{host}:{port}/{database}".format(
        flavor='postgresql',
        user=props['db_user'],
        password=props['db_password'],
        host=props['db_host'],
        port=props['db_port'],
        database=props['db_name']
    )
    return engine_info
