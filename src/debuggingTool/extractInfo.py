from PyQt5.QtWidgets import QLineEdit, QComboBox, QGroupBox, QTextEdit
import json, os

class InfoExtractor:
    def __init__(self, widgets, type):
        self.widgets = widgets
        self.reset_data()
        self.type = type

    def reset_data(self):
        self.extracted_data = {"inputs": [], "dropdowns": []}
        self.selected_analysis, self.library_data, self.subcircuit_data = None, [], []
        self.sources = {t: [] for t in ["pulse", "sine", "pwl", "ac", "DC", "exponential"]}

    def extract_text(self):
        self.reset_data()
        
        source_types = {
            "pulse": ["v1", "v2", "td", "tr", "tf", "pw", "tp"],
            "sine": ["vo", "va", "freq", "td", "theta"],
            "pwl": [],  # PWL is dynamic and doesn't have predefined parameters
            "ac": ["v_a", "p_a"],
            "DC": ["v_i"],
            "exponential": ["v1", "v2", "td1", "tau1", "td2", "tau2"]
        }
        
        current_source = None

        for widget in filter(lambda w: w.isVisible(), self.widgets):
            if isinstance(widget, QGroupBox):
                title = widget.title().strip()

                if "Analysis" in title:
                    self.selected_analysis = title.replace(" Analysis", "").upper()

                elif "Add library for" in title:
                    parts = title.replace("Add library for", "").strip().split(":")
                    component, device = parts[0].split()[-1], parts[1] if len(parts) == 2 else "Unknown"
                    entry = {"device": device.strip(), "component": component, "library": None}
                    if "mos" in device.lower():
                        entry["W"], entry["L"], entry["M"] = None, None, None
                    self.library_data.append(entry)

                elif "Add subcircuit for" in title:
                    self.subcircuit_data.append({"sub": title[18:].strip(), "dic": None})

                else:
                    for src_type in source_types:
                        if title.startswith(f"Add parameters for {src_type} source"):
                            # Save the previous PWL source before resetting
                            if current_source and current_source["source type"] == "pwl":
                                self.sources["pwl"].append(current_source)
                            
                            # Start new source
                            current_source = {"source type": src_type, "component": title[-2:]}
                            if src_type == "pwl":
                                current_source["value"] = []  # PWL values are stored as a list
                            break

            elif isinstance(widget, QLineEdit):
                text_value = widget.text().strip()

                # Store values for libraries
                for entry in self.library_data:
                    if entry["library"] is None:
                        entry["library"] = os.path.basename(text_value)
                        break
                    if "mos" in entry["device"].lower():
                        for param in ["W", "L", "M"]:
                            if entry.get(param) is None:
                                entry[param] = text_value
                                break

                # Store values for subcircuits
                for entry in self.subcircuit_data:
                    if entry["dic"] is None:
                        entry["dic"] = os.path.basename(text_value)
                        break

                # Store values for sources
                if current_source:
                    if current_source["source type"] == "pwl":
                        current_source["value"].append(text_value)  # Collect all PWL values
                    else:
                        for param in source_types[current_source["source type"]]:
                            if param not in current_source:
                                current_source[param] = text_value
                                break
                    
                    # Append the source when all expected values are filled (except for PWL)
                    if current_source["source type"] == "pwl":
                        pass  # Do nothing, let it accumulate values
                    # Ensure all parameters are collected before appending the source
                    expected_params = source_types.get(current_source["source type"], [])

                    # Check if we have collected all expected values
                    if current_source["source type"] == "DC" or (
                        expected_params and len([p for p in expected_params if p in current_source]) == len(expected_params)
                    ):
                        self.sources[current_source["source type"]].append(current_source)
                        current_source = None  # Reset after storing

                else:
                    self.extracted_data["inputs"].append(text_value)

            elif isinstance(widget, QComboBox):
                self.extracted_data["dropdowns"].append(widget.currentText().strip())

        # Ensure the last PWL source is added (for the last set of values)
        if current_source and current_source["source type"] == "pwl":
            self.sources["pwl"].append(current_source)

    def format(self):
        if self.type == 2:
            self.extract_text()
            formatted_output = {k + "_sources": v for k, v in self.sources.items() if v}

            if self.library_data:
                formatted_output["library"] = self.library_data
            if self.subcircuit_data:
                formatted_output["subcircuit"] = self.subcircuit_data

            if self.selected_analysis:
                analysis_keys = {
                    "TRANSIENT": ["Start Time", "Step Time", "Stop Time"],
                    "AC": ["Start Frequency", "Stop Frequency", "No. of Points"],
                    "DC": ["Source 1", "Start 1", "Increment 1", "Stop 1", "Source 2", "Start 2", "Increment 2", "Stop 2"]
                }

                values = self.extracted_data["inputs"]
                dropdown_values = self.extracted_data["dropdowns"]

                # AC Analysis: Extract units for Start and Stop Frequency
                if self.selected_analysis == "AC":
                    if len(values) >= 2 and len(dropdown_values) >= 2:
                        formatted_output["analysis"] = {
                            "Selected Analysis": self.selected_analysis,
                            "Start Frequency": values[0].strip(),
                            "Start Frequency Unit": dropdown_values[0].strip(),
                            "Stop Frequency": values[1].strip(),
                            "Stop Frequency Unit": dropdown_values[1].strip(),
                            "No. of Points": values[2] if len(values) > 2 else ""
                        }
                # DC Analysis: Extract units for Start, Increment, and Stop (for Source 1 and Source 2)
                elif self.selected_analysis == "DC":
                    formatted_output["analysis"] = {
                        "Selected Analysis": self.selected_analysis,
                        "Source 1": values[0].strip(),
                        "Start 1": values[1].strip(),
                        "Start 1 Unit": dropdown_values[0].strip(),
                        "Increment 1": values[2].strip(),
                        "Increment 1 Unit": dropdown_values[1].strip(),
                        "Stop 1": values[3].strip(),
                        "Stop 1 Unit": dropdown_values[2].strip(),
                        "Source 2": values[4].strip(),
                        "Start 2": values[5].strip(),
                        "Start 2 Unit": dropdown_values[3].strip(),
                        "Increment 2": values[6].strip(),
                        "Increment 2 Unit": dropdown_values[4].strip(),
                        "Stop 2": values[7].strip(),
                        "Stop 2 Unit": dropdown_values[5].strip()
                    }
                # Transient Analysis: Extract units for Start Time, Step Time, Stop Time
                elif self.selected_analysis == "TRANSIENT":
                    formatted_output["analysis"] = {
                        "Selected Analysis": self.selected_analysis,
                        "Start Time": values[0].strip(),
                        "Start Time Unit": dropdown_values[0].strip(),
                        "Step Time": values[1].strip(),
                        "Step Time Unit": dropdown_values[1].strip(),
                        "Stop Time": values[2].strip(),
                        "Stop Time Unit": dropdown_values[2].strip()
                    }
                else:
                    formatted_output["analysis"] = {
                        "Selected Analysis": self.selected_analysis,
                        **dict(zip(analysis_keys[self.selected_analysis], values + dropdown_values))
                    }

            print(formatted_output)
            return json.dumps(formatted_output, indent=4) if formatted_output else "{}"

        if self.type == 1:
            for widget in self.widgets:
                if isinstance(widget, QTextEdit):
                    return widget.toPlainText().strip()