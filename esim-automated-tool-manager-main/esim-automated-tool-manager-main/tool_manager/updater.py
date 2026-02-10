RECOMMENDED_VERSIONS = {
    "Ngspice": "39",
    "KiCad": "7"
}

def check_update(tool_name, current_version):
    recommended = RECOMMENDED_VERSIONS.get(tool_name)
    if not recommended or not current_version:
        return False, None
    if recommended not in current_version:
        return True, recommended
    return False, None
