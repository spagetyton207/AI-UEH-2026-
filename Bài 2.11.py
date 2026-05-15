import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

distance = ctrl.Antecedent(np.arange(0, 51, 1), 'distance')
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')
demand = ctrl.Antecedent(np.arange(0, 101, 1), 'demand')
weather = ctrl.Antecedent(np.arange(0, 101, 1), 'weather')
rating = ctrl.Antecedent(np.arange(1, 5.1, 0.1), 'rating')
punctuality = ctrl.Antecedent(np.arange(0, 101, 1), 'punctuality')

price = ctrl.Consequent(np.arange(0, 101, 1), 'price')
bonus = ctrl.Consequent(np.arange(0, 101, 1), 'bonus')

distance['short'] = fuzz.trimf(distance.universe, [0, 0, 3])
distance['medium'] = fuzz.trimf(distance.universe, [3, 4.5, 6])
distance['long'] = fuzz.trimf(distance.universe, [6, 13, 20])
distance['very_long'] = fuzz.trimf(distance.universe, [15, 32.5, 50])

traffic['low'] = fuzz.trimf(traffic.universe, [0, 15, 30])
traffic['medium'] = fuzz.trimf(traffic.universe, [20, 45, 70])
traffic['high'] = fuzz.trimf(traffic.universe, [60, 80, 100])

demand['low'] = fuzz.trimf(demand.universe, [0, 15, 30])
demand['medium'] = fuzz.trimf(demand.universe, [20, 45, 70])
demand['high'] = fuzz.trimf(demand.universe, [60, 80, 100])

weather['good'] = fuzz.trimf(weather.universe, [0, 0, 40])
weather['moderate'] = fuzz.trimf(weather.universe, [30, 50, 70])
weather['bad'] = fuzz.trimf(weather.universe, [60, 100, 100])

rating['poor'] = fuzz.trimf(rating.universe, [1.0, 1.75, 2.5])
rating['average'] = fuzz.trimf(rating.universe, [2.5, 3.25, 4.0])
rating['good'] = fuzz.trimf(rating.universe, [3.5, 4.25, 5.0])

punctuality['late'] = fuzz.trimf(punctuality.universe, [0, 25, 50])
punctuality['on_time'] = fuzz.trimf(punctuality.universe, [40, 60, 80])
punctuality['early'] = fuzz.trimf(punctuality.universe, [70, 85, 100])

price.automf(names=['low', 'medium', 'high', 'very_high'])
bonus.automf(names=['none', 'few', 'moderate', 'high'])

rule1 = ctrl.Rule(distance['short'] & traffic['low'] & demand['low'], price['low'])
rule2 = ctrl.Rule(distance['short'] & traffic['medium'] & demand['high'], price['medium'])
rule3 = ctrl.Rule(distance['medium'] & traffic['high'] & demand['high'], price['high'])
rule4 = ctrl.Rule(distance['long'] & traffic['medium'] & weather['good'], price['medium'])
rule5 = ctrl.Rule(distance['long'] & traffic['high'] & weather['bad'], price['very_high'])
rule6 = ctrl.Rule(distance['very_long'] & traffic['high'] & demand['high'], price['very_high'])
rule7 = ctrl.Rule(distance['medium'] & traffic['low'] & demand['low'], price['medium'])
rule8 = ctrl.Rule(distance['short'] & traffic['high'] & weather['bad'], price['high'])
rule9 = ctrl.Rule(distance['very_long'] & weather['bad'], price['very_high'])
rule10 = ctrl.Rule(distance['medium'] & traffic['medium'] & weather['moderate'], price['medium'])

rule11 = ctrl.Rule(rating['good'] & punctuality['early'], bonus['high'])
rule12 = ctrl.Rule(rating['average'] & punctuality['on_time'], bonus['moderate'])
rule13 = ctrl.Rule(rating['poor'] & punctuality['late'], bonus['none'])
rule14 = ctrl.Rule(distance['long'] & traffic['high'] & punctuality['on_time'], bonus['high'])
rule15 = ctrl.Rule(distance['medium'] & traffic['medium'] & rating['good'], bonus['moderate'])
rule16 = ctrl.Rule(rating['poor'] & punctuality['late'], bonus['none'])
rule17 = ctrl.Rule(distance['very_long'] & weather['bad'] & rating['good'], bonus['high'])
rule18 = ctrl.Rule(distance['short'] & rating['average'] & punctuality['on_time'], bonus['few'])
rule19 = ctrl.Rule(distance['long'] & traffic['high'] & punctuality['late'], bonus['few'])
rule20 = ctrl.Rule(distance['medium'] & weather['moderate'] & rating['good'], bonus['moderate'])

pricing_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
])
pricing_sim = ctrl.ControlSystemSimulation(pricing_ctrl)

pricing_sim.input['distance'] = 18
pricing_sim.input['traffic'] = 85
pricing_sim.input['demand'] = 75
pricing_sim.input['weather'] = 80
pricing_sim.input['rating'] = 4.0
pricing_sim.input['punctuality'] = 50

pricing_sim.compute()
print(f"Mức giá đề xuất (0-100): {pricing_sim.output['price']:.2f}")
print(f"Điểm thưởng đề xuất (0-100): {pricing_sim.output['bonus']:.2f}")