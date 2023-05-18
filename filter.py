import pandas as pd
import numpy as np

def filter_normal_ranges(mimic_data):
    """
    Clean abnormal values.
    """
    mask_saO2_range = mimic_data["SaO2"] <= 500
    mask_spO2_range = (mimic_data["SpO2"] <= 100) & (mimic_data["SpO2"] >=55)
    mimic_data_w_normal_target_ranges = mimic_data.loc[mask_saO2_range & mask_spO2_range]
    print("Keeping saO2 =< 500 and 100 <= SpO2 <= 55")
    print(mimic_data.shape, "to", mimic_data_w_normal_target_ranges.shape, sep="")

    print("Only keep within 30 minutes SaO2, Sp02 pairs")
    mimic_data_w_simulatenous_measures = mimic_data_w_normal_target_ranges.loc[
        np.abs(mimic_data_w_normal_target_ranges["delta_SpO2"]) <= 30
        ]
    print(mimic_data_w_normal_target_ranges.shape, "to", mimic_data_w_simulatenous_measures.shape, sep="")

    mask_norepi_range = (
    (mimic_data_w_simulatenous_measures["norepinephrine_equivalent_dose"] <= 10) 
    | (mimic_data_w_simulatenous_measures["norepinephrine_equivalent_dose"].isna())
    )
    mimic_data_w_normal_norepi_range = mimic_data_w_simulatenous_measures.loc[mask_norepi_range]
    print("Keeping norepinephrine_equivalent_dose <= 10")
    print("Final number of patients: ",len(mimic_data_w_normal_norepi_range))

    return mimic_data_w_normal_norepi_range
