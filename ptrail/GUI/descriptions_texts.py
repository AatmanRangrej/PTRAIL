

# In command palate dropdown combo box hover text description
module_selection_combobox = 'Choose between desired modules'

open_file_btn = 'Load the dataset.'

export_file_btn = 'Save the dataset.'

# Declare the dictionary to hold the feature descriptions to display as the tooltip
# (hover texts in dropdown menu).
feature_descriptions = {
            'Kinematic Features': "Derived features for enhancing the predictive power of machine learning algorithms.",
            'Temporal Features': 'Essential for understanding the time-based behavior of individuals and groups in '
                                 'mobility data.',
            'Filtering': 'Removes the noise and irregularities in the data.',
            'Interpolation': 'Fills large gaps in data points by using various techniques.',
            'Statistics': 'Converts the trajectory data into segment-based form.'
    }


filt_features_descriptions = {
            'Hampel Filter': 'detects and removes the outliers of the input data by using the Hampel identifier.',
            'Remove Duplicates': 'Duplicate Removal.',
            'By Trajectory ID': 'Filtering based on Trajectory ID.',
            'By Bounding Box': 'Filtering based on Bounding Box.',
            'By Date': 'Filtering based on Date.',
            'By DateTime': 'Filtering based on DateTime.',
            'By Maximum Speed': 'Filtering based on Max Speed.',
            'By Minimum Speed': 'Filtering based on Min Speed.',
            'By Minimum Consecutive Distance': 'Filtering based on Minimum Consecutive Distance.',
            'By Maximum Consecutive Distance': 'Filtering based on Maximum Consecutive Distance.',
            'By Maximum Distance and Speed': 'Filtering based on Maximum Distance and Speed.',
            'By Minimum Distance and Speed': 'Filtering based on Minimum Distance and Speed.',
            'Remove Outliers by Consecutive Distance': 'Removing Outliers based on Consecutive Distance.',
            'Remove Outliers by Consecutive Speed': 'Removing Outliers based on Consecutive Speed.',
            'Remove Trajectories with Less Points': 'Removing Trajectories with Less data points',
}


ip_features_descriptions = {
            'Linear Interpolation': 'Linear Interpolation',
            'Cubic Interpolation': 'Cubic Interpolation',
            'Kinematic Interpolation': 'Kinematic Interpolation',
            'Random-Walk Interpolation': 'Random-Walk Interpolation'
}


kinematic_features_descriptions = {
    'All Kinematic Features': 'All Kinematic features.',
    'Distance': 'Distance between consecutive points.',
    'Distance from Start': 'Distance from the start of the trajectory.',
    'Point within Range': 'Point within Range.',
    'Distance from Co-ordinates': 'Distance from a specific coordinate point.',
    'Speed': 'Speed',
    'Acceleration': 'Acceleration',
    'Jerk': 'Jerk',
    'Bearing': 'Bearing',
    'Bearing Rate': 'Bearing Rate',
    'Rate of Bearing Rate': 'Rate of Bearing Rate',
}

stat_features_descriptions = {
    'Segment Trajectories': 'Segmenting trajectory based on time interval.',
    'Generate Kinematic Statistics': 'Generating statistic based on kinematic features.',
    'Pivot Statistics DF': 'Converting the data to segment based representation'
}

temporal_features_descriptions = {
    'All Temporal Features': 'All Temporal Feature.',
    'Date': 'Date Extraction.',
    'Time': 'Time Extraction.',
    'Day of the Week': 'Day of the Week Extraction.',
    'Weekend Indicator': 'Weekend Indicator.',
    'Time of Day': 'Time of Day Extraction.'
}


