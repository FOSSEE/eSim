import numpy as np
import tensorflow as tf
import pandas as pd
import pickle
import joblib
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
class ErrorLogDebug:
    def __init__(self, log):
        self.log = log
        init_path = os.getcwd()
        new_dir = os.path.join(os.path.dirname(init_path), "debuggingTool/model/")
        # Load the trained neural network model
        self.model = load_model(new_dir+'ngspice_error_classifier.h5')

        # Load metadata
        with open(new_dir+'metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
            self.max_sequence_length = metadata['max_length']
            self.tokenizer = metadata['tokenizer']
            self.label_encoder = metadata['label_encoder']

        # Load Random Forest model and encoders
        self.rf_model = joblib.load(new_dir+"random_forest_model.pkl")
        self.error_type_encoder = joblib.load(new_dir+"error_type_encoder.pkl")
        self.netlist_component_encoder = joblib.load(new_dir+"netlist_component_encoder.pkl")
        self.suggestion_encoder = joblib.load(new_dir+"suggestion_encoder.pkl")

        # Extract error message and relevant line
        self.error_message, self.line = self.extract_error_message()

    @tf.function(reduce_retracing=True)
    def model_predict(self, processed_message):
        return self.model(processed_message, training=False)

    def extract_error_message(self):
        """Extracts the error message and relevant netlist line from the log."""
        if self.log:
            log_lines = self.log.split("\n")
            for i, line in enumerate(log_lines):
                if "Error on line" in line:
                    next_lines = log_lines[i + 1:]  # Get all lines after "Error on line"
                    filtered_lines = [l.strip() for l in next_lines if l.strip()]  # Remove empty lines
                    
                    if filtered_lines:
                        return filtered_lines[-1], filtered_lines[-2]  # Last non-empty line and preceding line
                else:
                    return self.log, "unknown"
        
        return "Unknown error", "unknown"

    def preprocess_error_message(self, message):
        """Tokenizes and pads the error message."""
        input_seq = self.tokenizer.texts_to_sequences([message])
        input_pad = pad_sequences(input_seq, maxlen=self.max_sequence_length)
        return input_pad

    def extract_component_or_source(self, error_type):
        """Extracts the component/source type or analysis type from the relevant log line.
        If no specific line is found, it assigns a component based on the error type.
        """
        if not self.line or self.line == "unknown":
            # Assign default component based on error type
            if error_type == "Invalid DC analysis statement":
                return "DC analysis"
            elif error_type == "Shorted Voltage Source":
                return "Voltage Source"
            elif error_type=="Invalid command error":
                return "NGSpice Command"
            elif error_type=="Control Card Error":
                return "Control Statement"
            
            elif error_type == "Short circuit error":
                return "esim components"
            elif error_type == "Unknown Subcircuit Error":
                # Extract last word from the first line of the error log
                first_line = self.log.split("\n")[0]
            
                last_word = first_line.split()[-1] if first_line.split() else "Unknown component"
                print(last_word)
                return last_word  # Return the last word as the component type
            return "Unknown component"
        

        line = self.line.lower()
        components = {'r': "Resistor", 'c': "Capacitor", 'j': "Jfet", 'q': "Transistor",'d':"Diode",
                      'l': "Inductor", 'm': "Mosfet", 'i': "DC Current Source"}
        sources = {"pulse": "Pulse voltage source", "pwl": "PWL Voltage Source",
                   "ac": "AC Voltage Source", "exp": "Exp Voltage Source",
                   "dc": "DC Voltage Source", "sine": "Sine voltage source"}

        if line.startswith(tuple(components.keys())):
            return components[line[0]]
        if line.startswith('v'):
            for key, value in sources.items():
                if key in line:
                    return value
        if line.startswith('.dc'):
            return "DC analysis"
        if line.startswith('.tran'):
            return ".tran analysis statement"
        if line.startswith('.ac'):
            return "AC analysis"

        return "Unknown component"

    def suggest(self):
        """Predicts the error type and generates a suggestion based on the component type."""
        if self.error_message=="Unknown error":
            return f"Simulation failed\n\nSuggestion: Make sure the circuit has valid control block and analysis statement."
        else:
            processed_message = self.preprocess_error_message(self.error_message)

            # Predict error type using the neural network model
            error_type_prob = self.model.predict(processed_message)
            error_type = self.label_encoder.inverse_transform([np.argmax(error_type_prob)])[0]

            # Extract component/source type (pass error_type to handle missing error lines)
            component_type = self.extract_component_or_source(error_type)

            # Prepare features for Random Forest model
            features = np.array([[error_type, component_type]])  # Ensure it's a 2D array
            features_df = pd.DataFrame(features, columns=["error_type", "component_type"])
            
            # Encode categorical features
            try:
                features_df["error_type"] = self.error_type_encoder.transform(features_df["error_type"])
                features_df["component_type"] = self.netlist_component_encoder.transform(features_df["component_type"])
            except ValueError:
                return f"Simulation failed\n\nError Type: {error_type}\n\nSuggestion: No suggestion available (Unknown component or error type)"

            # Rename columns to match the names used during model training
            features_df.rename(columns={"error_type": "error_type_encoded", "component_type": "netlist_component_encoded"}, inplace=True)

            # Predict suggestion using Random Forest model
            suggestion_encoded = self.rf_model.predict(features_df)
            suggestion = self.suggestion_encoder.inverse_transform(suggestion_encoded)[0]

            # Include the netlist error line in the suggestion if available
            netlist_info = f"\nNetlist Line: {self.line}" if self.line and self.line != "unknown" else ""

            return f"Simulation Failed\n\nError Type: {error_type}\n\nSuggestion: {suggestion}{netlist_info}"
