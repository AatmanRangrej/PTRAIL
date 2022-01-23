"""
    This class is used to connect the PTRAIL GUI to PTRAIL
    backend. All the GUI's functionalities are handled in this
    class.

    | Authors: Yaksh J Haranwala
"""
import random
import re

import folium

import inspect
import pandas as pd
import ptrail.utilities.constants as const

from PyQt5 import QtWidgets
from ptrail.GUI.Table import TableModel
from ptrail.GUI.InputDialog import InputDialog
from ptrail.core.TrajectoryDF import PTRAILDataFrame

from ptrail.features.kinematic_features import KinematicFeatures
from ptrail.features.temporal_features import TemporalFeatures
from ptrail.features.semantic_features import SemanticFeatures
from ptrail.preprocessing.statistics import Statistics
from ptrail.preprocessing.filters import Filters


class GuiHandler:
    def __init__(self, filename, window):
        self._window = window
        self._data = None
        self._model = None
        self._table = None

        self.display_df(filename=filename)
        self.add_map()

    def display_df(self, filename):
        """
            Display the DataFrame on the DFPane of the GUI.

            Parameters
            ----------
                filename: str
                    The name of the file. This is obtained from the GUI.

            Returns
            -------
                None
        """
        try:
            # First, we clear out the DF pane area.
            # This is done in order to make sure that 2 dataframes
            # are not loaded simultaneously making the view cluttered.
            for i in reversed(range(self._window.DFPane.count())):
                item = self._window.DFPane.itemAt(i)
                if isinstance(item, QtWidgets.QTableView):
                    item.widget().close()

                # remove the item from layout
                self._window.DFPane.removeItem(item)

            # Create the input dialog item.
            input_dialog = InputDialog(parent=self._window,
                                       labels=['Trajectory ID: ', 'DateTime: ', 'Latitude: ', 'Longitude: '],
                                       title='Enter the column names: ')

            # Get the input before displaying the dataframe.
            if input_dialog.exec():
                # Get the column names.
                col_names = input_dialog.getInputs()

                # Read the data into a PTRAIL dataframe.
                self._data = PTRAILDataFrame(data_set=pd.read_csv(filename),
                                             traj_id=col_names[0].strip(),
                                             datetime=col_names[1].strip(),
                                             latitude=col_names[2].strip(),
                                             longitude=col_names[3].strip())
                # Set the table model and display the dataframe.
                self._table = QtWidgets.QTableView()

                # NOTE: whenever we update DFs, make sure to send the data after resetting
                #       index and setting inplace as False.
                self._model = TableModel(self._data.reset_index(inplace=False))
                self._table.setModel(self._model)
                self._window.DFPane.addWidget(self._table)
                self._window.run_stats_btn.setEnabled(True)

        except AttributeError:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle("Incorrect Column names")
            msg.setText("Incorrect Column names provided.\n"
                        "Please Enter the names again.")
            msg.exec()
            self.__init__(filename, self._window)

    def add_map(self, weight: float = 3, opacity: float = 0.8):
        """
            Use folium to plot the trajectory on a map.
            Parameters
            ----------
                weight: float
                    The weight of the trajectory line on the map.
                opacity: float
                    The opacity of the trajectory line on the map.
            Returns
            -------
                folium.folium.Map
                    The map with plotted trajectory.
        """
        sw = self._data[['lat', 'lon']].min().values.tolist()
        ne = self._data[['lat', 'lon']].max().values.tolist()

        # Create a map with the initial point.
        map_ = folium.Map(location=(self._data.latitude[0], self._data.longitude[0]),
                          zoom_start=13)

        ids_ = list(self._data.traj_id.value_counts().keys())
        colors = ["#" + ''.join([random.choice('123456789BCDEF') for j in range(6)])
                  for i in range(len(ids_))]

        for i in range(len(ids_)):
            # First, filter out the smaller dataframe.
            small_df = self._data.reset_index().loc[self._data.reset_index()[const.TRAJECTORY_ID] == ids_[i],
                                                    [const.LAT, const.LONG]]

            # # Then, create (lat, lon) pairs for the data points.
            locations = []
            for j in range(len(small_df)):
                locations.append((small_df['lat'].iloc[j], small_df['lon'].iloc[j]))


            # Create text frame.
            iframe = folium.IFrame(f'<font size="1px">Trajectory ID: {ids_[i]} ' + '<br>' +
                                   f'Latitude: {locations[0][0]}' + '<br>' +
                                   f'Longitude: {locations[0][1]} </font>')

            # Create start and end markers for the trajectory.
            popup = folium.Popup(iframe, min_width=180, max_width=200, max_height=75)

            folium.Marker([small_df['lat'].iloc[0], small_df['lon'].iloc[0]],
                          color='green',
                          popup=popup,
                          marker_color='green',
                          icon=folium.Icon(icon_color='green', icon='circle', prefix='fa')).add_to(map_)

            # Create text frame.
            iframe = folium.IFrame(f'<font size="1px">Trajectory ID: {ids_[i]} ' + '<br>' +
                                   f'Latitude: {locations[0][0]}' + '<br>' +
                                   f'Longitude: {locations[0][1]} </font>')

            # Create start and end markers for the trajectory.
            popup = folium.Popup(iframe, min_width=180, max_width=200, max_height=75)

            folium.Marker([small_df['lat'].iloc[-1], small_df['lon'].iloc[-1]],
                          color='green',
                          popup=popup,
                          marker_color='red',
                          icon=folium.Icon(icon_color='red', icon='circle', prefix='fa')).add_to(map_)

            # Add trajectory to map.
            # folium.PolyLine(locations,
            #                 color=colors[i],
            #                 weight=weight,
            #                 opacity=opacity,).add_to(map_)

        map_.fit_bounds([sw, ne])
        self._window.map.setHtml(map_.get_root().render())

    def run_command(self):
        if self._window.feature_type.currentIndex() == 0:
            self._run_filters()
        elif self._window.feature_type.currentIndex() == 1:
            self._run_ip()
        elif self._window.feature_type.currentIndex() == 2:
            self._run_kinematic()
        elif self._window.feature_type.currentIndex() == 3:
            self._run_stats()
        else:
            self._run_temporal()

    def _run_ip(self):
        pass

    def _run_kinematic(self):
        """
            Here, we run the Kinematic features that the user selected
            and then send the answers back.

            Returns
            -------
                PTRAILDataFrame
        """
        selected_function = self._window.listWidget.selectedItems()[0].text()
        print(selected_function)

        # Based on the function selected by the user and whether it contains any
        # user given parameters, we will go ahead and run those features and update
        # the GUI with the results.

        if selected_function == 'All Kinematic Features':
            self._data = KinematicFeatures.generate_kinematic_features(self._data)

        elif selected_function == 'Distance':
            self._data = KinematicFeatures.create_distance_column(self._data)

        elif selected_function == 'Distance from Start':
            self._data = KinematicFeatures.create_distance_from_start_column(self._data)

        elif selected_function == 'Point within Range':
            params = inspect.getfullargspec(KinematicFeatures.create_point_within_range_column).args
            params.remove('dataframe')
            input_dialog = InputDialog(parent=self._window,
                                       labels=params,
                                       title='Enter parameters: ')
            if input_dialog.exec_():
                args = input_dialog.getInputs()

                # Use Regex to get all the digits from the coords input and convert
                # it to required tuple to feed into the method.
                temp = re.findall(r'\d+', args[0])
                coords = tuple(map(int, temp))

                dist_range = float(args[1])
                self._data = KinematicFeatures.create_point_within_range_column(self._data,
                                                                                coordinates=coords,
                                                                                dist_range=dist_range)
        elif selected_function == 'Distance from Co-ordinates':
            params = inspect.getfullargspec(KinematicFeatures.create_distance_from_point_column).args
            params.remove('dataframe')
            input_dialog = InputDialog(parent=self._window,
                                       labels=params,
                                       title='Enter parameters: ')
            if input_dialog.exec_():
                args = input_dialog.getInputs()

                # Use Regex to get all the digits from the coords input and convert
                # it to required tuple to feed into the method.
                temp = re.findall(r'\d+', args[0])
                coords = tuple(map(int, temp))

                self._data = KinematicFeatures.create_distance_from_point_column(dataframe=self._data,
                                                                                 coordinates=coords,)

        elif selected_function == 'Speed':
            self._data = KinematicFeatures.create_speed_column(self._data)

        elif selected_function == 'Acceleration':
            self._data = KinematicFeatures.create_acceleration_column(self._data)

        elif selected_function == 'Jerk':
            self._data = KinematicFeatures.create_jerk_column(self._data)

        elif selected_function == 'Bearing':
            self._data = KinematicFeatures.create_bearing_column(self._data)

        elif selected_function == 'Bearing Rate':
            self._data = KinematicFeatures.create_bearing_rate_column(self._data)

        elif selected_function == 'Rate of Bearing Rate':
            self._data = KinematicFeatures.create_rate_of_br_column(self._data)

        # Finally, update the GUI with the updated DF received from the
        # function results. DO NOT FORGET THE reset_index(inplace=False).
        self._model = TableModel(self._data.reset_index(inplace=False))
        self._table.setModel(self._model)

    def _run_temporal(self):
        pass

    def _run_filters(self):
        pass

    def _run_stats(self):
        pass
