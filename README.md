# NMA2020_Steinmetz_RL_decision
This package uses the Steinmetz dataset to study decision making that involves trial history information.

# 2020-07-20
## Contents
* load_data.py
   * Loads the Steinmetz dataset
* RL_model.py
   
* ecoding_model.py
* plottings.py
* Steinmetz_RL_decision.ipynb
    * visualize the trial history effect in decision making (Lak et al. 2019)
    * call functions in `RL_model` to extract V_L and V_R as the hallmark of history effect
    * call functions in `plottings` to visualize neural activity as a function of V_L/V_R and P_L/P_R
    * call functions in `encoding_model` to build, fit and cross-validate encoding models with or without VL/VR

# 2020-07-22
Switched a project.
## Contents:
* load_data.py
* GPFA_synthetic_data.py
* GPFA_caller.ipynb