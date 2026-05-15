import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

rating = ctrl.Antecedent(np.arange(1, 5.1, 0.1), 'rating')
sales_volume = ctrl.Antecedent(np.arange(0, 1001, 1), 'sales_volume')
margin = ctrl.Antecedent(np.arange(0, 101, 1), 'margin')
seasonal = ctrl.Antecedent(np.arange(0, 101, 1), 'seasonal')
competitor = ctrl.Antecedent(np.arange(0, 101, 1), 'competitor')

discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

rating['low'] = fuzz.trimf(rating.universe, [1.0, 2.5, 4.0])
rating['medium'] = fuzz.trimf(rating.universe, [4.0, 4.25, 4.5])
rating['high'] = fuzz.trimf(rating.universe, [4.5, 5.0, 5.0])

sales_volume['low'] = fuzz.trimf(sales_volume.universe, [0, 0, 300])
sales_volume['medium'] = fuzz.trimf(sales_volume.universe, [200, 500, 800])
sales_volume['high'] = fuzz.trimf(sales_volume.universe, [700, 1000, 1000])

margin['low'] = fuzz.trimf(margin.universe, [0, 0, 30])
margin['medium'] = fuzz.trimf(margin.universe, [20, 50, 80])
margin['high'] = fuzz.trimf(margin.universe, [70, 100, 100])

seasonal['none'] = fuzz.trimf(seasonal.universe, [0, 0, 30])
seasonal['moderate'] = fuzz.trimf(seasonal.universe, [20, 50, 80])
seasonal['high'] = fuzz.trimf(seasonal.universe, [70, 100, 100])

competitor['low'] = fuzz.trimf(competitor.universe, [0, 0, 30])
competitor['medium'] = fuzz.trimf(competitor.universe, [20, 50, 80])
competitor['high'] = fuzz.trimf(competitor.universe, [70, 100, 100])

discount['very_low'] = fuzz.trimf(discount.universe, [0, 2.5, 5])
discount['low'] = fuzz.trimf(discount.universe, [5, 7.5, 10])
discount['medium'] = fuzz.trimf(discount.universe, [10, 15, 20])
discount['high'] = fuzz.trimf(discount.universe, [20, 30, 40])
discount['very_high'] = fuzz.trimf(discount.universe, [40, 55, 70])

rule1 = ctrl.Rule(rating['high'] & sales_volume['high'] & margin['high'], discount['very_low'])
rule2 = ctrl.Rule(rating['low'] & sales_volume['low'] & margin['high'], discount['high'])
rule3 = ctrl.Rule(seasonal['high'] & competitor['high'], discount['very_high'])
rule4 = ctrl.Rule(rating['medium'] & sales_volume['medium'] & margin['medium'], discount['medium'])
rule5 = ctrl.Rule(competitor['low'] & margin['low'] & sales_volume['high'], discount['very_low'])
rule6 = ctrl.Rule(rating['low'] & seasonal['none'], discount['medium'])
rule7 = ctrl.Rule(sales_volume['low'] & margin['low'], discount['very_high'])

discount_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
discount_sim = ctrl.ControlSystemSimulation(discount_ctrl)

discount_sim.input['rating'] = 4.3
discount_sim.input['sales_volume'] = 500
discount_sim.input['margin'] = 15
discount_sim.input['seasonal'] = 85
discount_sim.input['competitor'] = 90

discount_sim.compute()

print(f"Mức chiết khấu đề xuất (%): {discount_sim.output['discount']:.2f}%")