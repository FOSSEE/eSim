import json
import re
import os
class DetectAndSuggest:
    def __init__(self, formatted,netlist):
        """Initialize the class with formatted input data and load the valid device data from 'lib.json'."""
        init_path = os.getcwd()
        new_dir = os.path.join(os.path.dirname(init_path), "debuggingTool/")
        self.formatted = json.loads(formatted)
        with open(new_dir+'lib.json', 'r') as file:
            self.valid_data = json.load(file)
        try:
            with open(netlist, 'r') as file:
                self.netlist = file.read()  # Read entire content instead of using readlines()
        except Exception as e:
                    print("Failed to read netlist file.")
    
    @staticmethod
    def convert_to_microns(value):
        """Convert user input values with units (e.g., '100u', '1m', '180n') into micrometers (µm)."""
        match = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*(u|m|n)?$", value.lower().strip()) if value else None
        if not match:
            return None
        num, unit = float(match[1]), match[2]
        return num * {'m': 1000, 'n': 0.001}.get(unit, 1)

    def validate_mosfet(self):
        """Validate all MOSFET parameters (L, W, M) in the provided data."""
        messages = []
        
        for entry in self.formatted.get("library", []):
            if "mos" in entry.get("device", "").lower():
                name, component = entry.get("device", "Unknown"), entry.get("component", "Unknown")
                valid_entry = next((item for item in self.valid_data.get("library", []) if item.get("device") == name), None)
                if not valid_entry:
                    messages.append(f"Error: Device '{name}' is not recognized in the library. Please verify the device name.")
                    continue

                L, W, M = entry.get("L", "").strip(), entry.get("W", "").strip(), entry.get("M", "").strip()
                L_microns, W_microns = self.convert_to_microns(L), self.convert_to_microns(W)
                valid_L, valid_W = valid_entry.get("L", []), valid_entry.get("W", [])

                if M and (not M.isdigit() or int(M) <= 0):
                    messages.append(f"Error: Device '{component}' has an invalid multiplier (M). It must be a positive integer greater than zero.")
                
                for param, microns, valid_values in [("L", L_microns, valid_L), ("W", W_microns, valid_W)]:
                    if entry.get(param):
                        if microns is None:
                            messages.append(f"Error: Device '{component}' has an invalid {param} value. Ensure it follows the correct format, e.g., '180n', '0.5u', or '1m'.")
                        elif microns <= 0:
                            messages.append(f"Error: Device '{component}' has an invalid {param}. The value must be greater than zero.")
                        elif valid_values and microns not in valid_values:
                            messages.append(f"Error: Device '{component}' has an unacceptable {param} value. Acceptable values are {valid_values} µm.")
        
        return "\n".join(messages) if messages else ""
            
    def validate_analysis_inputs(self):
        """Validate numerical inputs for analysis parameters and enforce correct formats."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})
        analysis_type = analysis_data.get("Selected Analysis", "")
        
        if analysis_type:
            keys = {
                "TRANSIENT": ["Start Time", "Step Time", "Stop Time"],
                "AC": ["Start Frequency", "Stop Frequency", "No. of Points"],
                "DC": ["Source 1", "Start 1", "Increment 1", "Stop 1", "Source 2", "Start 2", "Increment 2", "Stop 2"]
            }
            
            if analysis_type == "DC":
                source_1 = analysis_data.get("Source 1", "").strip()
                source_2 = analysis_data.get("Source 2", "").strip()
                
                if not source_1 and not source_2:
                    messages.append("Error: At least one source (Source 1 or Source 2) must be provided for DC analysis.")
                else:
                    for i in range(1, 3):
                        if analysis_data.get(f"Source {i}", "").strip():
                            for param in ["Start", "Increment", "Stop"]:
                                key = f"{param} {i}"
                                value = analysis_data.get(key, "").strip()
                                if not value:
                                    messages.append(f"Warning: Field '{key}' is empty. Please provide a value.")
                                elif not re.match(r"^-?\d+(\.\d+)?$", value):
                                    messages.append(f"Error: '{key}' must be a numeric value without units.")
                                
            else:
                for key in keys.get(analysis_type, []):
                    value = analysis_data.get(key, "").strip()

                    # Check for empty value
                    if not value:
                        messages.append(f"Warning: Field '{key}' is empty. Please provide a value.")
                    elif key in ["Start Frequency", "Stop Frequency","Start Time","Step Time","Stop Time"]:
                        # Ensure the value is numeric and check for negative values
                        try:
                            float_value = float(value)  # Try to convert to float
                            if float_value < 0:
                                messages.append(f"Error: '{key}' must be a positive value. Negative values are not allowed.")
                        except ValueError:
                            messages.append(f"Error: '{key}' must be a numeric value without units. Use the dropdown for unit selection.")
                    elif key == "No. of Points":
                        if not value.isdigit() or int(value) <= 0:
                            messages.append(f"Error: '{key}' must be a positive integer.")
                    
                    elif not re.match(r"^-?\d+(\.\d+)?$", value):
                        messages.append(f"Error: '{key}' must be a numeric value without units. Use the dropdown for unit selection.")
        
        return "\n".join(messages) if messages else ""
    def validate_ac_analysis_sources(self):
        """Ensure the circuit has at least one AC or SINE source when AC analysis is selected."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})

        if analysis_data.get("Selected Analysis") == "AC":
            # Extract all sources from the netlist
            sources = [
                line for line in self.netlist.splitlines()
                if line.strip() and re.match(r"^[ivIV]", line.strip())  # Match sources (V or I)
            ]
           
            # Check if at least one source is AC or SINE
            ac_sources = [src for src in sources if "AC" in src.upper() or "SINE" in src.upper()]
            print(ac_sources)
            if not ac_sources:
                messages.append("Error: If you want to analyze a circuit using AC analysis, you must include at least one AC sinusoidal source.")

        return "\n".join(messages) if messages else ""

    def validate_transient_analysis(self):
        """Validate that Start Time < Stop Time and convert values into numeric."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})
        start_time = analysis_data.get("Start Time", "").strip()
        start_unit = analysis_data.get("Start Time Unit", "").strip()
        stop_time = analysis_data.get("Stop Time", "").strip()
        stop_unit = analysis_data.get("Stop Time Unit", "").strip()

        # Check if Start and Stop times are valid first
        if start_time and stop_time:
            try:
                start_time_val = self.convert_to_time(start_time, start_unit)
                stop_time_val = self.convert_to_time(stop_time, stop_unit)

                if start_time_val is None or stop_time_val is None:
                    messages.append("Error: Invalid time format. Use numeric values with valid units (sec, ms, us, ns, ps).")
                elif start_time_val >= stop_time_val:
                    messages.append(f"Error: Start Time must be less than Stop Time.Increase Stop Time or decrease Start Time. Example: Start = {start_time} {start_unit}, Stop = {float(start_time) * 10} {start_unit}")
            except ValueError:
                messages.append("Error: Invalid time format. Use numeric values with valid units (sec, ms, us, ns, ps).")
        
        return "\n".join(messages) if messages else ""
   
        
    def validate_sources(self):
        """Validate source values and warn users about empty fields, setting 0 as the default."""
        messages = []
        for source_type, sources in self.formatted.items():
            if source_type.endswith("_sources"):
                for source in sources:
                    for key, value in source.items():
                        if key != "source type":
                            if isinstance(value, list):  # Check if it's a list
                                if not value or all(isinstance(v, str) and v.strip() == "" for v in value):
                                    messages.append(f"Warning: Field '{key}' in {source['source type']} source is empty. Default value [0] will be inserted.")
                                    source[key] = ["0"]
                            elif isinstance(value, str):  # Ensure it's a string before using strip()
                                if value.strip() == "":
                                    messages.append(f"Warning: Field '{key}' in {source['source type']} source is empty. Default value 0 will be inserted.")
                                    source[key] = "0"
                            elif value is None:  # Handle NoneType
                                messages.append(f"Warning: Field '{key}' in {source['source type']} source is empty. Default value 0 will be inserted.")
                                source[key] = "0"

        return "\n".join(messages) if messages else ""



    def convert_to_hz(self,value, unit):
        """Convert frequency values with units (Hz, KHz, MHz, GHz, THz) into Hz."""
        unit_multipliers = {"Hz": 1, "KHz": 1e3, "Meg": 1e6, "GHz": 1e9, "THz": 1e12}
        try:
            num = float(value.strip())
            return num * unit_multipliers.get(unit.strip(), 1)  # Default to Hz if unit is missing
        except ValueError:
            return None  # Invalid format
    def convert_to_time(self,value, unit):
        """Convert user input values with time units (sec, ms, us, ns, ps) into seconds."""
        time_multipliers = {
            "sec": 1,
            "ms": 1e-3,
            "us": 1e-6,
            "ns": 1e-9,
            "ps": 1e-12
        }
        try:
            num = float(value.strip())
            return num * time_multipliers.get(unit.strip(), 1)  # Default to sec if unit is missing
        except ValueError:
            return None  # Invalid format

    def validate_analysis_frequencies(self):
        """Check that Stop Frequency is greater than Start Frequency if the format is valid."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})
        start_freq = analysis_data.get("Start Frequency", "").strip()
        start_unit = analysis_data.get("Start Frequency Unit", "").strip()
        stop_freq = analysis_data.get("Stop Frequency", "").strip()
        stop_unit = analysis_data.get("Stop Frequency Unit", "").strip()

        # Check if Start and Stop frequencies are valid first
        if start_freq and stop_freq:
            # Check for negative values
            if float(start_freq) <= 0:
                messages.append("Error: 'Start Frequency' must be a positive value. Zero and Negative values are not allowed.")
            if float(stop_freq) < 0:
                messages.append("Error: 'Stop Frequency' must be a positive value. Negative values are not allowed.")
            
            # Proceed with conversion to Hz if there are no negative values
            if not any("Error" in message for message in messages):  # Only proceed if no negative values were found
                start_freq_hz = self.convert_to_hz(start_freq, start_unit)
                stop_freq_hz = self.convert_to_hz(stop_freq, stop_unit)

                if start_freq_hz is None or stop_freq_hz is None:
                    messages.append("Error: Invalid frequency format. Use numeric values with valid units (Hz, KHz, MHz, GHz, THz).")
                elif start_freq_hz >= stop_freq_hz:
                    messages.append(f"Error: Start Frequency must be less than Stop Frequency.Increase Stop Frequency or decrease Start Frequency. Example: Start = {start_freq} {start_unit}, Stop = {float(start_freq) * 10} {start_unit}")

        return "\n".join(messages) if messages else ""
      
    def validate_library_and_subcircuits(self):
        """Validate library and subcircuit names against predefined valid entries."""
        messages = []
        
        def validate(entry, valid_list, key, entry_type):
            name, file_name = entry.get(key, "").strip(), entry.get("dic" if entry_type == "subcircuit" else "library", "").strip()
            valid_entry = next((item for item in valid_list if item.get(key) == name), None)
            valid_files = valid_entry.get("dic" if entry_type == "subcircuit" else "library", []) if valid_entry else []
            
            if not file_name:
                messages.append(f"Error: {entry_type.capitalize()} for '{name}' is missing. Please ensure the correct file is provided.\n")
            elif not valid_files:
                messages.append(f"Error: {entry_type.capitalize()} for '{name}' is not recognized in the valid list.\n")
            elif file_name not in valid_files:
                messages.append(f"Error: {entry_type.capitalize()} for '{name}' has an invalid file '{file_name}'. Expected one of {valid_files}.\n")
        
        for entry_type in ["subcircuit", "library"]:
            for entry in self.formatted.get(entry_type, []):
                validate(entry, self.valid_data.get(entry_type, []), "sub" if entry_type == "subcircuit" else "device", entry_type)
        
        return "\n".join(messages) if messages else ""
    

    def validate_user_selected_sources(self):
        """Ensure Source 1 and Source 2 specified by the user exist in the netlist and are either voltage or current sources."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})
        
        if analysis_data.get("Selected Analysis") == "DC":
            source_1 = analysis_data.get("Source 1", "").strip().lower()
            source_2 = analysis_data.get("Source 2", "").strip().lower()
            
            # Print the user-provided sources for debugging
            print(f"User-selected Source 1: '{source_1}', Source 2: '{source_2}'")
            
            # Extract all sources from the netlist
            sources = {
                re.split(r"\s+", line.strip())[0].lower(): line  # Store source name in lowercase for comparison
                for line in self.netlist.splitlines()
                if line.strip() and re.match(r"^[ivIV]", line.strip().lower())  # Match lines starting with 'I' or 'V'
            }
            
            # Print the extracted sources for debugging
            print(f"Extracted Sources from Netlist: {sources}")
            
            # Check if the user-selected sources exist in the netlist and are valid
            for src_name, src_value in [("Source 1", source_1), ("Source 2", source_2)]:
                if src_value and src_value not in sources:
                    messages.append(f"Error: {src_name} ('{src_value}') is not a voltage or current source in the netlist.")
        
        # Return any error messages or an empty string if there are no errors
        return "\n".join(messages) if messages else ""


    def convert_to_numeric(self,value, unit):
            """Convert user input values with units into their base values (Volts or Amperes)."""
            unit_multipliers = {
                "Volts or Amperes": 1,
                "mV or mA": 1e-3,
                "uV or uA": 1e-6,
                "nV or nA": 1e-9,
                "pV or pA": 1e-12
            }
            try:
                num = float(value.strip())
                return num * unit_multipliers.get(unit.strip(), 1)  # Default to base unit if missing
            except ValueError:
                return None  # Invalid format

    def validate_dc_analysis(self):
        """Validate DC analysis parameters including increment direction and zero increment warning."""
        messages = []
        analysis_data = self.formatted.get("analysis", {})
        
        if analysis_data.get("Selected Analysis") == "DC":
            for i in range(1, 3):
                source = analysis_data.get(f"Source {i}", "").strip()
                start = analysis_data.get(f"Start {i}", "").strip()
                stop = analysis_data.get(f"Stop {i}", "").strip()
                increment = analysis_data.get(f"Increment {i}", "").strip()
                unit = analysis_data.get(f"Unit {i}", "").strip()
                
                if source:
                    start_val = self.convert_to_numeric(start, unit)
                    stop_val = self.convert_to_numeric(stop, unit)
                    increment_val = self.convert_to_numeric(increment, unit)
                    
                    if None in (start_val, stop_val, increment_val):
                        continue  # Skip if conversion failed, already handled in other validation
                    
                    if increment_val == 0:
                        messages.append(f"Warning: Increment value for {source} is zero. It must be non-zero to avoid an infinite loop.")
                    elif start_val < stop_val and increment_val < 0:
                        messages.append(f"Error: Increment for {source} is negative while Start < Stop. Increment must be positive in this case.")
                    elif start_val > stop_val and increment_val > 0:
                        messages.append(f"Error: Increment for {source} is positive while Start > Stop. Increment must be negative in this case.")
        
        return "\n".join(messages) if messages else ""
    
    def validate_ng(self):
        """Validate all parameters and return proper messages."""
        messages = []
        
        messages.append(self.validate_ac_analysis_sources())
        if not any("Error" in msg for msg in messages):
            messages.append(self.validate_analysis_inputs())
        if not any("Error" in msg for msg in messages):
            messages.append(self.validate_analysis_frequencies())
            messages.append(self.validate_transient_analysis())
        messages.append(self.validate_library_and_subcircuits())
        messages.append(self.validate_mosfet())
        messages.append(self.validate_sources())
        messages.append(self.validate_user_selected_sources())
        messages.append(self.validate_dc_analysis())  # Added DC analysis validation
        messages = list(filter(None, messages))
        return "All inputs are valid. No errors detected." if not messages else "\n".join(messages)
