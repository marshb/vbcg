#!/usr/bin/env python
# settings.py - tool for reading/storing settings of the main program

import ConfigParser
import io
import numpy as np
import logging

from defines import *

std_param = [VAL_WEBCAM, VAL_CAMERA, VAL_ALGORITHM, VAL_CURVES, VAL_FRAMES, VAL_TRIGGER, VAL_MOTION, VAL_FACE]

# Load parameters from configuration file
def get_parameters():

    # Load the configuration file
    try:
        with open('settings.ini') as f:
            sample_config = f.read()
        config = ConfigParser.RawConfigParser()
        config.readfp(io.BytesIO(sample_config))
    except IOError:
        logging.warning("Settings file not found! Creating one with standard values.")
        __store_parameters(std_param)
    except:
        logging.critical("Unexpected error")

    # Store data from configuration file in array
    param = np.zeros(8)
    i = 0

    # Read settings
    options = config.options('settings')
    # Iterate throughout each option
    for option in options:
        # Store value in array
        param[i] = config.get('settings',option)
        # Increase counter
        i += 1

    # Return parameters
    return param

# Flip a boolean value in parameters
def flip_parameter(idx):

    # Get parameters
    param = get_parameters()

    # Flip boolean value
    param[idx] = 1 - param[idx]

    # Log to file
    tmp_str = "Parameter: %d was changed" % (idx)
    logging.info(tmp_str)

    # Store in file
    __store_parameters(param)

    # Return parameters
    return param

# Change a non-boolean value in parameters
def change_parameter(idx,val):

    # Get parameters
    param = get_parameters()

    # Change parameter value
    param[idx] = val

    # Store in file
    __store_parameters(param)

    # Return parameters
    return param

# Store parameters in file
def __store_parameters(param):

    # Open file
    config_file = open('settings.ini', 'w')
    config = ConfigParser.ConfigParser(allow_no_value = True)

    # Add content
    config.add_section('settings')

    config.set('settings', '# use webcam or frames from hard disk?')    # Comment
    config.set('settings', 'bool_use_webcam', param[0])                 # Parameter

    config.set('settings', '# use which camera port?')                  # ...
    config.set('settings', 'idx_camera', param[1])                      # ...

    config.set('settings', '# use which algorithm?')
    config.set('settings', 'idx_algorithm', param[2])

    config.set('settings', '# Show curves?')
    config.set('settings', 'bool_show_curves', param[3])

    config.set('settings', '# Store frames on hard disk?')
    config.set('settings', 'bool_store_frames', param[4])

    config.set('settings', '# Trigger the MRI via serial port?')
    config.set('settings', 'bool_use_triggerbox', param[5])

    config.set('settings', '# Use motion detection?')
    config.set('settings', 'bool_use_motion_detection', param[6])

    config.set('settings', '# Use viola jones algorithm?')
    config.set('settings', 'bool_use_face_detection', param[7])


    # Write and close file
    config.write(config_file)
    config_file.close()

    return 0