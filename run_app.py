"""
Launcher script for the Talent Management System Streamlit app
This script makes it easy to run the app from the root directory
"""
import streamlit.web.cli as stcli
import os
import sys

if __name__ == "__main__":
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Path to the main.py file
    main_script = os.path.join(dir_path, "app", "main.py")
    
    # Launch the app
    sys.argv = ["streamlit", "run", main_script]
    sys.exit(stcli.main())
