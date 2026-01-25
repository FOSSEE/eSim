# ngspiceSimulation/data_extraction.py
"""
Data extraction module for NGSpice simulation results.

This module handles the extraction and processing of simulation data from NGSpice
output files, supporting AC, DC, and Transient analysis types.
"""

import os
import logging
from decimal import Decimal
from typing import List, Tuple, Dict, Any, Optional
from PyQt5 import QtWidgets
from configuration.Appconfig import Appconfig

# Set up logging
logger = logging.getLogger(__name__)


class DataExtraction:
    """
    Extracts and processes simulation data from NGSpice output files.
    
    This class handles reading and parsing voltage and current data from
    NGSpice simulation output files for different analysis types.
    """
    
    # Analysis type constants
    AC_ANALYSIS = 0
    TRANSIENT_ANALYSIS = 1
    DC_ANALYSIS = 2

    def __init__(self) -> None:
        """Initialize the DataExtraction instance."""
        self.obj_appconfig = Appconfig()
        self.data: List[str] = []
        # consists of all the columns of data belonging to nodes and branches
        self.y: List[List[Decimal]] = []  # stores y-axis data
        self.x: List[Decimal] = []  # stores x-axis data
        # Add the missing instance variables
        self.NBList: List[str] = []
        self.NBIList: List[str] = []
        self.volts_length: int = 0

    def numberFinder(self, file_path: str) -> List[int]:
        """
        Analyze simulation files to determine data structure parameters.
        
        Args:
            file_path: Path to the directory containing simulation files
            
        Returns:
            List containing [lines_per_node, voltage_nodes, analysis_type, 
                           dec_flag, current_branches]
        """
        # Opening Analysis file
        with open(os.path.join(file_path, "analysis")) as analysis_file:
            self.analysisInfo = analysis_file.read()
        self.analysisInfo = self.analysisInfo.split(" ")

        # Reading data file for voltage
        with open(os.path.join(file_path, "plot_data_v.txt")) as voltage_file:
            self.voltData = voltage_file.read()

        self.voltData = self.voltData.split("\n")

        # Initializing variable
        # 'lines_per_node' gives no. of lines of data for each node/branch
        # 'partitions_per_voltage_node' gives the no of partitions for a single voltage node
        # 'voltage_node_count' gives total number of voltage
        # 'current_branch_count' gives total number of current

        lines_per_node = partitions_per_voltage_node = voltage_node_count = current_branch_count = 0

        # Finding total number of voltage node
        for line in self.voltData[3:]:
            # it has possible names of voltage nodes in NgSpice
            if "Index" in line:  # "V(" in line or "x1" in line or "u3" in line:
                voltage_node_count += 1

        # Reading Current Source Data
        with open(os.path.join(file_path, "plot_data_i.txt")) as current_file:
            self.currentData = current_file.read()
        self.currentData = self.currentData.split("\n")

        # Finding Number of Branch
        for line in self.currentData[3:]:
            if "#branch" in line:
                current_branch_count += 1

        self.dec = 0

        # For AC
        if self.analysisInfo[0][-3:] == ".ac":
            self.analysisType = self.AC_ANALYSIS
            if "dec" in self.analysisInfo:
                self.dec = 1

            for line in self.voltData[3:]:
                lines_per_node += 1  # 'lines_per_node' gives no. of lines of data for each node/branch
                if "Index" in line:
                    partitions_per_voltage_node += 1
                # 'partitions_per_voltage_node' gives the no of partitions for a single voltage node
                logger.debug(f"partitions_per_voltage_node: {partitions_per_voltage_node}")
                if "AC" in line:  # DC for dc files and AC for ac ones
                    break

        elif ".tran" in self.analysisInfo:
            self.analysisType = self.TRANSIENT_ANALYSIS
            for line in self.voltData[3:]:
                lines_per_node += 1
                if "Index" in line:
                    partitions_per_voltage_node += 1
                # 'partitions_per_voltage_node' gives the no of partitions for a single voltage node
                logger.debug(f"partitions_per_voltage_node: {partitions_per_voltage_node}")
                if "Transient" in line:  # DC for dc files and AC for ac ones
                    break

        # For DC:
        else:
            self.analysisType = self.DC_ANALYSIS
            for line in self.voltData[3:]:
                lines_per_node += 1
                if "Index" in line:
                    partitions_per_voltage_node += 1
                # 'partitions_per_voltage_node' gives the no of partitions for a single voltage node
                logger.debug(f"partitions_per_voltage_node: {partitions_per_voltage_node}")
                if "DC" in line:  # DC for dc files and AC for ac ones
                    break

        voltage_node_count = voltage_node_count // partitions_per_voltage_node  # voltage_node_count gives the no of voltage nodes
        current_branch_count = current_branch_count // partitions_per_voltage_node  # current_branch_count gives the no of branches

        analysis_params = [lines_per_node, voltage_node_count, self.analysisType, self.dec, current_branch_count]

        return analysis_params

    def openFile(self, file_path: str) -> List[int]:
        """
        Open and process simulation data files.
        
        Args:
            file_path: Path to the directory containing simulation files
            
        Returns:
            List containing [analysis_type, dec_flag]
            
        Raises:
            Exception: If files cannot be read or processed
        """
        try:
            with open(os.path.join(file_path, "plot_data_i.txt")) as current_file:
                all_current_data = current_file.read()

            all_current_data = all_current_data.split("\n")
            self.NBIList = []

            with open(os.path.join(file_path, "plot_data_v.txt")) as voltage_file:
                all_voltage_data = voltage_file.read()

        except Exception as e:
            logger.error(f"Exception reading files: {e}")
            self.obj_appconfig.print_error(f'Exception Message: {e}')
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Unable to open plot data files.')
            self.msg.exec_()

        try:
            try:
                for token in all_current_data[3].split(" "):
                    if len(token) > 0:
                        self.NBIList.append(token)
                self.NBIList = self.NBIList[2:]
                current_list_length = len(self.NBIList)
            except (IndexError, AttributeError) as e:
                logger.warning(f"Error parsing current data: {e}")
                self.NBIList = []
                current_list_length = 0
        except Exception as e:
            logger.error(f"Exception parsing current data: {e}")
            self.obj_appconfig.print_error(f'Exception Message: {e}')
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Unable to read Analysis File.')
            self.msg.exec_()

        data_params = self.numberFinder(file_path)
        lines_per_partition = int(data_params[0] + 1)
        voltage_node_count = int(data_params[1])
        analysis_type = data_params[2]
        current_branch_count = data_params[4]

        analysis_info = [analysis_type, data_params[3]]
        self.NBList = []
        all_voltage_data = all_voltage_data.split("\n")
        for token in all_voltage_data[3].split(" "):
            if len(token) > 0:
                self.NBList.append(token)
        self.NBList = self.NBList[2:]
        voltage_list_length = len(self.NBList)
        logger.info(f"NBLIST: {self.NBList}")

        processed_current_data = []
        voltage_column_count = len(all_voltage_data[5].split("\t"))
        current_column_count = len(all_current_data[5].split("\t"))

        full_data = []

        # Creating list of data:
        if analysis_type < 3:
            for voltage_node_index in range(1, voltage_node_count):
                for token in all_voltage_data[3 + voltage_node_index * lines_per_partition].split(" "):
                    if len(token) > 0:
                        self.NBList.append(token)
                self.NBList.pop(voltage_list_length)
                self.NBList.pop(voltage_list_length)
                voltage_list_length = len(self.NBList)

            for current_branch_index in range(1, current_branch_count):
                for token in all_current_data[3 + current_branch_index * lines_per_partition].split(" "):
                    if len(token) > 0:
                        self.NBIList.append(token)
                self.NBIList.pop(current_list_length)
                self.NBIList.pop(current_list_length)
                current_list_length = len(self.NBIList)

            partition_row_index = 0
            data_row_index = 0
            combined_row_index = 0

            for line in all_current_data[5:lines_per_partition - 1]:
                if len(line.split("\t")) == current_column_count:
                    current_row = line.split("\t")
                    current_row.pop(0)
                    current_row.pop(0)
                    current_row.pop()
                    if analysis_type == 0:  # not in trans
                        current_row.pop()

                    for current_partition_index in range(1, current_branch_count):
                        additional_current_line = all_current_data[5 + current_partition_index * lines_per_partition + data_row_index].split("\t")
                        additional_current_line.pop(0)
                        additional_current_line.pop(0)
                        if analysis_type == 0:
                            additional_current_line.pop()  # not required for dc
                        additional_current_line.pop()
                        current_row = current_row + additional_current_line

                    full_data.append(current_row)

                data_row_index += 1

            for line in all_voltage_data[5:lines_per_partition - 1]:
                if len(line.split("\t")) == voltage_column_count:
                    voltage_row = line.split("\t")
                    voltage_row.pop()
                    if analysis_type == 0:
                        voltage_row.pop()
                    for voltage_partition_index in range(1, voltage_node_count):
                        additional_voltage_line = all_voltage_data[5 + voltage_partition_index * lines_per_partition + partition_row_index].split("\t")
                        additional_voltage_line.pop(0)
                        additional_voltage_line.pop(0)
                        if analysis_type == 0:
                            additional_voltage_line.pop()  # not required for dc
                        if self.NBList[len(self.NBList) - 1] == 'v-sweep':
                            self.NBList.pop()
                            additional_voltage_line.pop()

                        additional_voltage_line.pop()
                        voltage_row = voltage_row + additional_voltage_line
                    voltage_row = voltage_row + full_data[combined_row_index]
                    combined_row_index += 1

                    combined_row_str = "\t".join(voltage_row[1:])
                    combined_row_str = combined_row_str.replace(",", "")
                    self.data.append(combined_row_str)

                partition_row_index += 1

        self.volts_length = len(self.NBList)
        self.NBList = self.NBList + self.NBIList

        logger.info(f"Analysis info: {analysis_info}")
        return analysis_info

    def numVals(self) -> List[int]:
        """
        Get the number of data columns and voltage nodes.
        
        Returns:
            List containing [total_columns, voltage_node_count]
        """
        total_columns = len(self.data[0].split("\t"))
        voltage_node_count = self.volts_length
        return [total_columns, voltage_node_count]

    def computeAxes(self) -> None:
        """
        Compute x and y axis data from the processed simulation data.
        
        This method extracts the time/frequency data (x-axis) and 
        voltage/current data (y-axis) from the processed data.
        """
        if not self.data:
            logger.warning("No data available for axis computation")
            return

        num_columns = len(self.data[0].split("\t"))
        self.y = []
        first_row_values = self.data[0].split("\t")
        for column_index in range(1, num_columns):
            self.y.append([Decimal(first_row_values[column_index])])
        for row in self.data[1:]:
            row_values = row.split("\t")
            for column_index in range(1, num_columns):
                self.y[column_index - 1].append(Decimal(row_values[column_index]))
        for row in self.data:
            row_values = row.split("\t")
            self.x.append(Decimal(row_values[0]))
