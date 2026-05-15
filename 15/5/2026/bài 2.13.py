import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

product_demand = ctrl.Antecedent(np.arange(0, 101, 1), 'product_demand')
competitor_pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'competitor_pressure')
store_reputation = ctrl.Antecedent(np.arange(1, 5.1, 0.1), 'store_reputation')
profit_margin = ctrl.Antecedent(np.arange(0, 101, 1), 'profit_margin')
seasonal_demand = ctrl.Antecedent(np.arange(0, 101, 1), 'seasonal_demand')

discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

for var in [product_demand, competitor_pressure, profit_margin]:
    var['low'] = fuzz.trimf(var.universe, [0, 0, 40])
    var['medium'] = fuzz.trimf(var.universe, [20, 50, 80])
    var['high'] = fuzz.trimf(var.universe, [60, 100, 100])

seasonal_demand['none'] = fuzz.trimf(seasonal_demand.universe, [0, 0, 40])
seasonal_demand['medium'] = fuzz.trimf(seasonal_demand.universe, [20, 50, 80])
seasonal_demand['high'] = fuzz.trimf(seasonal_demand.universe, [60, 100, 100])

store_reputation['low'] = fuzz.trimf(store_reputation.universe, [1.0, 2.5, 4.0])
store_reputation['medium'] = fuzz.trimf(store_reputation.universe, [4.0, 4.25, 4.5])
store_reputation['high'] = fuzz.trimf(store_reputation.universe, [4.5, 5.0, 5.0])

discount['very_low'] = fuzz.trimf(discount.universe, [0, 2.5, 5])
discount['low'] = fuzz.trimf(discount.universe, [5, 7.5, 10])
discount['medium'] = fuzz.trimf(discount.universe, [10, 15, 20])
discount['high'] = fuzz.trimf(discount.universe, [20, 30, 40])
discount['very_high'] = fuzz.trimf(discount.universe, [40, 55, 70])

rule1 = ctrl.Rule(product_demand['high'] & competitor_pressure['low'] & profit_margin['low'], discount['very_low'])
rule2 = ctrl.Rule(product_demand['low'] & competitor_pressure['high'] & profit_margin['high'], discount['high'])
rule3 = ctrl.Rule(store_reputation['high'] & profit_margin['medium'] & seasonal_demand['high'], discount['medium'])
rule4 = ctrl.Rule(competitor_pressure['high'] & seasonal_demand['high'] & profit_margin['high'], discount['very_high'])
rule5 = ctrl.Rule(store_reputation['low'] & product_demand['medium'] & profit_margin['low'], discount['medium'])
rule6 = ctrl.Rule(product_demand['high'] & seasonal_demand['none'] & competitor_pressure['low'], discount['very_low'])
rule7 = ctrl.Rule(profit_margin['high'] & competitor_pressure['medium'] & seasonal_demand['medium'], discount['medium'])

specialty_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
specialty_sim = ctrl.ControlSystemSimulation(specialty_ctrl)

specialty_sim.input['product_demand'] = 85
specialty_sim.input['competitor_pressure'] = 50
specialty_sim.input['store_reputation'] = 4.2
specialty_sim.input['profit_margin'] = 85
specialty_sim.input['seasonal_demand'] = 85

specialty_sim.compute()

print(f"Mức chiết khấu đề xuất (%): {specialty_sim.output['discount']:.2f}%")