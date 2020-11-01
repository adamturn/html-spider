"""
Python 3.8.5 64-bit
Author: Adam Turner <turner.adch@gmail.com>
"""
# standard library
import re


class Adjudicator(object):
    """Static validation methods that raise an error or return None."""

    @staticmethod
    def validate_names(names):
        """Ensures that we were able to parse aggregate flow data.
        
        Args:
            names: expects a list of strings
        """
        print("Validating names data...")
        entry_flow_regex = re.compile(r"^Aggregated\sEntry\sFlow$")
        exit_flow_regex = re.compile(r"^Aggregated\sExit\sFlow$")

        entry_flow, exit_flow = False, False    
        for name in names:
            if entry_flow_regex.search(name):
                if entry_flow:
                    raise ValueError(f"Names matched entry flow regex more than once. DEBUG: names : {names}")
                else:
                    entry_flow = True

            if exit_flow_regex.search(name):
                if exit_flow:
                    raise ValueError(f"Names matched exit flow regex more than once. DEBUG: values : {values}")
                else:
                    exit_flow = True

        if entry_flow and exit_flow:
            print("Data passed 'names' validation.")
            return None
        else:
            raise ValueError(f"Failed to match both aggregate flow names, test the 'names' list. DEBUG: names : {names}")
    
    @staticmethod
    def validate_values(values):
        """Ensures that parsed values have a valid float format.

        Args:
            values: expects a list of strings
        """
        print("Validating values data...")
        value_regex = re.compile(r"^\d+\.\d+$")

        for value in values:
            if value_regex.search(value):
                continue
            else:
                raise ValueError(f"Failed on value: {value}, test the 'values' list.")

        print("Data passed 'values' validation.")
        return None
