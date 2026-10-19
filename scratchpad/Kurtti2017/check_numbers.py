import math
import json
from pathlib import Path

k = 1.380649e-23
T = 300.0
q = 1.602176634e-19
c = 299792458.0
rf, ct, bw, z = 5000.0, 3e-12, 230e6, 100e3
sigma_t, slope = 155e-12, 62e6
noise_v = sigma_t * slope
noise_i = noise_v / z
results = {
    'bandwidth_from_1p5ns_MHz': 0.35 / 1.5e-9 / 1e6,
    'noise_voltage_from_jitter_mV': noise_v * 1e3,
    'noise_input_from_jitter_nArms': noise_i * 1e9,
    'noise_input_from_10mV_nArms': 10e-3 / z * 1e9,
    'threshold_sigma_from_recomputed_noise': 70e-3 / noise_v,
    'MDS_for_SNR10_uA': 10 * noise_i * 1e6,
    '100kOhm_dBOhm': 20 * math.log10(z),
    '10kOhm_dBOhm': 20 * math.log10(2 * rf),
    'post_gain': z / (2 * rf),
    'timing_DR_dB': 20 * math.log10(100000),
    'approx_linear_DR_dB': 20 * math.log10(100),
    'Rin_from_BW_ohm': 1 / (2 * math.pi * bw * ct),
    'A0_if_input_pole_only': 2 * math.pi * rf * ct * bw,
    'noise_zero_MHz': 1 / (2 * math.pi * rf * ct) / 1e6,
    'density_equivalents_pA': {str(b): 100e-9 / math.sqrt(b * bw) * 1e12 for b in [1, 1.11, math.pi / 2]},
    'RF_single_half_noise_pA': math.sqrt(4 * k * T / rf) * 1e12,
    'RF_differential_APD_noise_pA': math.sqrt(2 * k * T / rf) * 1e12,
    'RF_bound_single_half_ohm': 4 * k * T / (100e-9 / math.sqrt(bw))**2,
    'RF_fraction_single_half_percent': (4 * k * T / rf) / (100e-9 / math.sqrt(bw))**2 * 100,
    'B1_chain_OhmHz': z * bw,
    'B1_TIA_with_chain_BW_proxy_OhmHz': 2 * rf * bw,
    'B2_chain_totalCin': z * bw * ct,
    'B2_chain_Cpd_only': z * bw * 1.5e-12,
    'B3_chain_by_power': {str(p): z * bw / p for p in [150, 180, 300, 330]},
    'B6_voltage_noise_proxy_nV': (100e-9 / math.sqrt(bw)) * math.sqrt(3) / (2 * math.pi * bw * ct) * 1e9,
    'power_core_mW': (2 + 2) * 3.3,
    'power_one_post_branch_mW': 3 * 2 * 1.6 * 3.3,
    'power_core_two_post_branches_mW': (4 + 2 * 3 * 2 * 1.6) * 3.3,
    'receiver_current_mA_by_power': {str(p): p / 3.3 for p in [150, 180]},
    'distance_mm_by_time_ps': {str(t): c * t * 1e-12 / 2 * 1e3 for t in [25, 65, 140, 173, 175, 24, 50, 2500]},
    'standard_error_mean_at_175ps_N10000_ps': 175 / math.sqrt(10000),
    'optimal_N_paper_formula': 2 * math.log(10),
    'constant_slope_55to75mV_time_ps': (75e-3 - 55e-3) / slope * 1e12,
    'PIN_shot_10uA_pA': math.sqrt(2 * q * 10e-6) * 1e12,
    'APD_shot_10uA_M100_F1_pA': math.sqrt(2 * q * 10e-6 * 100) * 1e12,
    'assumed_CT_RF_CFcap_for230MHz_fF': 1 / (2 * math.pi * rf * bw) * 1e15,
    'wrong_100k_as_RF_required_GBW_GHz': 2 * math.pi * z * ct * bw**2 / 1e9,
    'actual_5k_half_RF_required_GBW_GHz_proxy': 2 * math.pi * rf * ct * bw**2 / 1e9,
}
gm_cases = []
for mu in [100e-6, 200e-6]:
    g1 = math.sqrt(2 * mu * (750 / 0.35) * 1e-3)
    g2 = math.sqrt(2 * mu * (300 / 0.35) * 1e-3)
    gp = math.sqrt(2 * mu * (75 / 0.35) * 1.6e-3)
    gl, gf = 1 / 700, 1 / 9000
    a0 = g1 * (g2 - gf) / (gl**2 + gf * (2 * gl + g2))
    ap = gp * 400 / (1 + gp * (118 / 2))
    gm_cases.append({'assumed_muCox_uA_V2': mu * 1e6, 'gm1_mS': g1 * 1e3,
                     'gm2_mS': g2 * 1e3, 'gm_post_mS': gp * 1e3,
                     'A0_no_ro_or_capacitance': a0,
                     'Rin_RF_over_A0_ohm': rf / a0,
                     'input_pole_if_A0_constant_MHz': a0 / (2 * math.pi * rf * ct) / 1e6,
                     'post_stage_gain': ap, 'post_three_stage_gain': ap**3})
results['gm_conditional_estimates'] = gm_cases
results['Cgs_fF_at_assumed_Cox3to5'] = {
    str(w): [(2 / 3) * w * 0.35 * co for co in [3, 5]] for w in [750, 300, 75]
}
text = json.dumps(results, ensure_ascii=False, indent=2)
Path(__file__).with_name('numbers.json').write_text(text, encoding='utf-8')
print(text)
