# API for the Sindex DLL (sindex64.dll) to calculate site index, age, height, and years to breast height.
# The DLL is used to calculate site index, age, height, and years to breast height for trees based on various parameters.
# Official documentation unavailable. The documentation here has been generated using GPT-4o and may contain errors.

import ctypes
from ctypes import c_double, c_short, c_char, c_int, POINTER, c_char_p, c_void_p, byref
import logging

import os

# Determine the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(current_dir, 'sindex64.dll')

# Load the DLL from the determined path
sindex_dll = ctypes.CDLL(dll_path)


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('sindex_log')
error_log = logging.getLogger('sindex_error')


class EnumCstIntFIZ:
    """
    Enumeration for Coastal or Interior FIZ zones.
    """
    COAST = 0
    INTERIOR = 1


class EnumSiteClass:
    """
    Enumeration for different site classes.
    """
    NONE = 0
    LOW = 1
    POOR = 2
    MEDIUM = 3
    GOOD = 4


class EAgeType:
    """
    Enumeration for types of age (Total or Breast Height).
    """
    TOTAL = 0
    BREAST = 1


class ERegen:
    """
    Enumeration for types of regeneration (Natural or Planted).
    """
    NATURAL = 0
    PLANTED = 1


class EEstimate:
    """
    Enumeration for estimation method (Iterate or Direct).
    """
    ITERATE = 0
    DIRECT = 1


# Helper methods to handle error codes
def get_sindex_err_msg(error_code):
    """
    Get the corresponding error message for a given error code.

    Args:
        error_code (int): The error code returned by a DLL function.

    Returns:
        str: A descriptive error message corresponding to the error code.
    """
    error_messages = {
        -1: "site index <= 1.3",
        -2: "bhage < 0.5 (for GI)",
        -3: "bhage > GI range",
        -4: "no answer was generated",
        -5: "input curve is not a valid curve index",
        -6: "site class is unknown",
        -7: "FIZ code is unknown",
        -8: "species code is unknown",
        -9: "total age and GI curve",
        -10: "source species index is not valid, or no conversion",
        -11: "unknown age type",
        -12: "input parameter is not a valid establishment type",
    }
    return error_messages.get(error_code, "unknown issue")


# Wrapper functions for each DLL function

def get_version_number():
    """
    Retrieve the version number of the Sindex DLL.

    Returns:
        float: The version number as a floating point value.
    """
    sindex_version_number = sindex_dll.Sindex_VersionNumber
    sindex_version_number.restype = c_short
    result = sindex_version_number()
    version = round(result / 100.0, 2)
    log.debug(f"Sindex_VersionNumber() -> {version}")
    return version


def get_first_species():
    """
    Retrieve the index of the first species available in the Sindex DLL.

    Returns:
        int: The index of the first species, or -1 if an error occurs.
    """
    sindex_first_species = sindex_dll.Sindex_FirstSpecies
    sindex_first_species.restype = c_short
    result = sindex_first_species()
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_FirstSpecies() -> Error: {msg}")
        return -1
    log.debug(f"Sindex_FirstSpecies() -> {result}")
    return result


def get_next_species(idx):
    """
    Retrieve the index of the next species based on the current species index.

    Args:
        idx (int): The current species index.

    Returns:
        int: The index of the next species, or -1 if there are no more species or an error occurs.
    """
    sindex_next_species = sindex_dll.Sindex_NextSpecies
    sindex_next_species.argtypes = [c_short]
    sindex_next_species.restype = c_short
    result = sindex_next_species(c_short(idx))
    if result == -4:
        log.debug("Sindex_NextSpecies() -> Last defined species index")
        return -1
    elif result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_NextSpecies({idx}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_NextSpecies({idx}) -> {result}")
    return result


def get_species_code(species_idx):
    """
    Retrieve the species code for a given species index.

    Args:
        species_idx (int): The species index.

    Returns:
        str: The species code as a string.
    """
    sindex_spec_code = sindex_dll.Sindex_SpecCode
    sindex_spec_code.argtypes = [c_short]
    sindex_spec_code.restype = c_char_p
    result = sindex_spec_code(c_short(species_idx)).decode().strip()
    log.debug(f"Sindex_SpecCode({species_idx}) -> {result}")
    return result


def get_species_name(species_idx):
    """
    Retrieve the species name for a given species index.

    Args:
        species_idx (int): The species index.

    Returns:
        str: The species name as a string.
    """
    sindex_spec_name = sindex_dll.Sindex_SpecName
    sindex_spec_name.argtypes = [c_short]
    sindex_spec_name.restype = c_char_p
    result = sindex_spec_name(c_short(species_idx)).decode().strip()
    log.debug(f"Sindex_SpecName({species_idx}) -> {result}")
    return result


def get_def_curve(species_idx):
    """
    Retrieve the default curve index for a given species.

    Args:
        species_idx (int): The species index.

    Returns:
        int: The default curve index, or -1 if an error occurs.
    """
    sindex_def_curve = sindex_dll.Sindex_DefCurve
    sindex_def_curve.argtypes = [c_short]
    sindex_def_curve.restype = c_short
    result = sindex_def_curve(c_short(species_idx))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_DefCurve({species_idx}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_DefCurve({species_idx}) -> {result}")
    return result


def get_def_curve_est(species_idx, regen_type):
    """
    Retrieve the default curve index for a given species based on the regeneration type.

    Args:
        species_idx (int): The species index.
        regen_type (int): The regeneration type (natural or planted).

    Returns:
        int: The default curve index, or -1 if an error occurs.
    """
    sindex_def_curve_est = sindex_dll.Sindex_DefCurveEst
    sindex_def_curve_est.argtypes = [c_short, c_short]
    sindex_def_curve_est.restype = c_short
    result = sindex_def_curve_est(c_short(species_idx), c_short(regen_type))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_DefCurveEst({species_idx}, {regen_type}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_DefCurveEst({species_idx}, {regen_type}) -> {result}")
    return result


def get_def_gi_curve(species_idx):
    """
    Retrieve the default growth intercept curve for a given species.

    Args:
        species_idx (int): The species index.

    Returns:
        int: The default growth intercept curve index, or -1 if an error occurs.
    """
    sindex_def_gi_curve = sindex_dll.Sindex_DefGICurve
    sindex_def_gi_curve.argtypes = [c_short]
    sindex_def_gi_curve.restype = c_short
    result = sindex_def_gi_curve(c_short(species_idx))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_DefGICurve({species_idx}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_DefGICurve({species_idx}) -> {result}")
    return result


def get_first_curve(species_idx):
    """
    Retrieve the first curve index for a given species.

    Args:
        species_idx (int): The species index.

    Returns:
        int: The first curve index, or -1 if an error occurs.
    """
    sindex_first_curve = sindex_dll.Sindex_FirstCurve
    sindex_first_curve.argtypes = [c_short]
    sindex_first_curve.restype = c_short
    result = sindex_first_curve(c_short(species_idx))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_FirstCurve({species_idx}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_FirstCurve({species_idx}) -> {result}")
    return result


def get_next_curve(species_idx, curve_idx):
    """
    Retrieve the next curve index for a given species and current curve index.

    Args:
        species_idx (int): The species index.
        curve_idx (int): The current curve index.

    Returns:
        int: The next curve index, or -1 if there are no more curves or an error occurs.
    """
    sindex_next_curve = sindex_dll.Sindex_NextCurve
    sindex_next_curve.argtypes = [c_short, c_short]
    sindex_next_curve.restype = c_short
    result = sindex_next_curve(c_short(species_idx), c_short(curve_idx))
    if result == -4:
        log.debug("Sindex_NextCurve() -> Last defined curve index for this species")
        return -1
    elif result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_NextCurve({species_idx}, {curve_idx}) -> Error: {msg}")
        return -1
    log.debug(f"Sindex_NextCurve({species_idx}, {curve_idx}) -> {result}")
    return result


def get_curve_name(curve_idx):
    """
    Retrieve the name of a curve given its index.

    Args:
        curve_idx (int): The curve index.

    Returns:
        str: The name of the curve.
    """
    sindex_curve_name = sindex_dll.Sindex_CurveName
    sindex_curve_name.argtypes = [c_short]
    sindex_curve_name.restype = c_char_p
    result = sindex_curve_name(c_short(curve_idx)).decode().strip()
    log.debug(f"Sindex_CurveName({curve_idx}) -> {result}")
    return result


def get_curve_source(curve_idx):
    """
    Retrieve the source of a curve given its index.

    Args:
        curve_idx (int): The curve index.

    Returns:
        str: The source of the curve.
    """
    sindex_curve_source = sindex_dll.Sindex_CurveSource
    sindex_curve_source.argtypes = [c_short]
    sindex_curve_source.restype = c_char_p
    result = sindex_curve_source(c_short(curve_idx)).decode().strip()
    log.debug(f"Sindex_CurveSource({curve_idx}) -> {result}")
    return result


def get_curve_notes(curve_idx):
    """
    Retrieve notes associated with a curve given its index.

    Args:
        curve_idx (int): The curve index.

    Returns:
        str: Notes associated with the curve.
    """
    sindex_curve_notes = sindex_dll.Sindex_CurveNotes
    sindex_curve_notes.argtypes = [c_short]
    sindex_curve_notes.restype = c_char_p
    result = sindex_curve_notes(c_short(curve_idx)).decode().strip()
    log.debug(f"Sindex_CurveNotes({curve_idx}) -> {result}")
    return result


def calc_site(species_idx, height, age, use_bh, estimate_type):
    """
    Calculate the site index based on height and age for a given species.

    Args:
        species_idx (int): The species index.
        height (float): The height of the tree.
        age (float): The age of the tree.
        use_bh (int): The type of age (Total or Breast Height).
        estimate_type (int): The estimation method (Iterate or Direct).

    Returns:
        float: The calculated site index, or negative infinity if an error occurs.
    """
    sindex_ht_age_to_si = sindex_dll.Sindex_HtAgeToSI
    sindex_ht_age_to_si.argtypes = [c_short, c_double, c_short, c_double, c_short, POINTER(c_double)]
    sindex_ht_age_to_si.restype = c_int

    site = c_double(0.0)
    result = sindex_ht_age_to_si(c_short(species_idx), c_double(age), c_short(use_bh), c_double(height),
                                 c_short(estimate_type), byref(site))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_HtAgeToSI({species_idx}, {age}, {use_bh}, {height}, {estimate_type}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_HtAgeToSI({species_idx}, {age}, {use_bh}, {height}, {estimate_type}) -> {site.value}")
    return site.value


def calc_age(curve_idx, site_index, height, yrs_to_breast_height, use_bh):
    """
    Calculate the age of a tree based on site index and height.

    Args:
        curve_idx (int): The curve index.
        site_index (float): The site index.
        height (float): The height of the tree.
        yrs_to_breast_height (float): The years to reach breast height.
        use_bh (int): The type of age (Total or Breast Height).

    Returns:
        float: The calculated age, or negative infinity if an error occurs.
    """
    sindex_ht_si_to_age = sindex_dll.Sindex_HtSIToAge
    sindex_ht_si_to_age.argtypes = [c_short, c_double, c_short, c_double, c_double, POINTER(c_double)]
    sindex_ht_si_to_age.restype = c_int

    age = c_double(0.0)
    result = sindex_ht_si_to_age(c_short(curve_idx), c_double(height), c_short(use_bh), c_double(site_index),
                                 c_double(yrs_to_breast_height), byref(age))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(
            f"Sindex_HtSIToAge({curve_idx}, {height}, {use_bh}, {site_index}, {yrs_to_breast_height}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_HtSIToAge({curve_idx}, {height}, {use_bh}, {site_index}, {yrs_to_breast_height}) -> {age.value}")
    return age.value


def calc_height(curve_idx, site_index, age, yrs_to_breast_height, use_bh):
    """
    Calculate the height of a tree based on site index and age.

    Args:
        curve_idx (int): The curve index.
        site_index (float): The site index.
        age (float): The age of the tree.
        yrs_to_breast_height (float): The years to reach breast height.
        use_bh (int): The type of age (Total or Breast Height).

    Returns:
        float: The calculated height, or negative infinity if an error occurs.
    """
    sindex_age_si_to_ht = sindex_dll.Sindex_AgeSIToHt
    sindex_age_si_to_ht.argtypes = [c_short, c_double, c_short, c_double, c_double, POINTER(c_double)]
    sindex_age_si_to_ht.restype = c_int

    height = c_double(0.0)
    result = sindex_age_si_to_ht(c_short(curve_idx), c_double(age), c_short(use_bh), c_double(site_index),
                                 c_double(yrs_to_breast_height), byref(height))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(
            f"Sindex_AgeSIToHt({curve_idx}, {age}, {use_bh}, {site_index}, {yrs_to_breast_height}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_AgeSIToHt({curve_idx}, {age}, {use_bh}, {site_index}, {yrs_to_breast_height}) -> {height.value}")
    return height.value


def calc_y2bh(curve_idx, site_index):
    """
    Calculate the years required for a tree to reach breast height.

    Args:
        curve_idx (int): The curve index.
        site_index (float): The site index.

    Returns:
        float: The years to reach breast height, or negative infinity if an error occurs.
    """
    sindex_y2bh = sindex_dll.Sindex_Y2BH
    sindex_y2bh.argtypes = [c_short, c_double, POINTER(c_double)]
    sindex_y2bh.restype = c_int

    yrs_to_breast_height = c_double(0.0)
    result = sindex_y2bh(c_short(curve_idx), c_double(site_index), byref(yrs_to_breast_height))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_Y2BH({curve_idx}, {site_index}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_Y2BH({curve_idx}, {site_index}) -> {yrs_to_breast_height.value}")
    return yrs_to_breast_height.value


def calc_convert_site(spec_idx, site_index, target_spec_idx):
    """
    Convert the site index from one species to another.

    Args:
        spec_idx (int): The source species index.
        site_index (float): The site index to convert.
        target_spec_idx (int): The target species index.

    Returns:
        float: The converted site index, or negative infinity if an error occurs.
    """
    sindex_si_to_si = sindex_dll.Sindex_SIToSI
    sindex_si_to_si.argtypes = [c_short, c_double, c_short, POINTER(c_double)]
    sindex_si_to_si.restype = c_int

    site = c_double(0.0)
    result = sindex_si_to_si(c_short(spec_idx), c_double(site_index), c_short(target_spec_idx), byref(site))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_SIToSI({spec_idx}, {site_index}, {target_spec_idx}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_SIToSI({spec_idx}, {site_index}, {target_spec_idx}) -> {site.value}")
    return site.value


def calc_site_class_to_site_index(species_idx, site_class, fiz):
    """
    Calculate the site index based on site class and FIZ.

    Args:
        species_idx (int): The species index.
        site_class (int): The site class (e.g., Low, Medium, Good).
        fiz (int): The FIZ zone (e.g., Coast or Interior).

    Returns:
        float: The calculated site index, or negative infinity if an error occurs.
    """
    sindex_sc_to_si = sindex_dll.Sindex_SCToSI
    sindex_sc_to_si.argtypes = [c_short, c_char, c_char, POINTER(c_double)]
    sindex_sc_to_si.restype = c_int

    site = c_double(0.0)
    result = sindex_sc_to_si(c_short(species_idx), c_char(site_class), c_char(fiz), byref(site))
    if result < 0:
        msg = get_sindex_err_msg(result)
        error_log.error(f"Sindex_SCToSI({species_idx}, {site_class}, {fiz}) -> Error: {msg}")
        return float('-inf')
    log.debug(f"Sindex_SCToSI({species_idx}, {site_class}, {fiz}) -> {site.value}")
    return site.value
