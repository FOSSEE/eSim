class TrackWidget:
    """
    - This Class track the dynamically created widget of KicadtoNgSpice Window.
    - Tracks using dictionary and lists ==>
        - Sources
        - Parameters
        - References
        - Model Details
        - ... etc
    - All attributes are class-level (shared across instances by design).
    - Call TrackWidget.reset() at the start of each conversion to clear
      accumulated state from previous runs.
    """
    # Track widget list for Source details
    sourcelisttrack = {"ITEMS": "None"}
    source_entry_var = {"ITEMS": "None"}

    # Track widget for analysis inserter details
    AC_entry_var = {"ITEMS": "None"}
    AC_Parameter = {"ITEMS": "None"}
    DC_entry_var = {"ITEMS": "None"}
    DC_Parameter = {"ITEMS": "None"}
    TRAN_entry_var = {"ITEMS": "None"}
    TRAN_Parameter = {"ITEMS": "None"}
    set_CheckBox = {"ITEMS": "None"}
    AC_type = {"ITEMS": "None"}
    op_check = []
    # Track widget for Model detail
    modelTrack = []
    microcontrollerTrack = []
    model_entry_var = {}
    microcontroller_var = {}

    # Track Widget for Device Model detail
    deviceModelTrack = {}

    # Track Widget for Subcircuits where directory has been selected
    subcircuitTrack = {}
    # Track subcircuits which are specified in .cir file
    subcircuitList = {}

    @classmethod
    def reset(cls):
        """Reset all shared class-level state for a fresh conversion run."""
        cls.sourcelisttrack = {"ITEMS": "None"}
        cls.source_entry_var = {"ITEMS": "None"}
        cls.AC_entry_var = {"ITEMS": "None"}
        cls.AC_Parameter = {"ITEMS": "None"}
        cls.DC_entry_var = {"ITEMS": "None"}
        cls.DC_Parameter = {"ITEMS": "None"}
        cls.TRAN_entry_var = {"ITEMS": "None"}
        cls.TRAN_Parameter = {"ITEMS": "None"}
        cls.set_CheckBox = {"ITEMS": "None"}
        cls.AC_type = {"ITEMS": "None"}
        cls.op_check = []
        cls.modelTrack = []
        cls.microcontrollerTrack = []
        cls.model_entry_var = {}
        cls.microcontroller_var = {}
        cls.deviceModelTrack = {}
        cls.subcircuitTrack = {}
        cls.subcircuitList = {}
