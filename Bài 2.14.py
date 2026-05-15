import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

density = ctrl.Antecedent(np.arange(0, 101, 1), 'density')
urgency = ctrl.Antecedent(np.arange(0, 101, 1), 'urgency')
load = ctrl.Antecedent(np.arange(0, 101, 1), 'load')
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')
profit = ctrl.Antecedent(np.arange(0, 101, 1), 'profit')

combine = ctrl.Consequent(np.arange(1, 11, 1), 'combine')
priority = ctrl.Consequent(np.arange(0, 101, 1), 'priority')

for var in [density, urgency, load, traffic, profit]:
    var['low'] = fuzz.trimf(var.universe, [0, 0, 45])
    var['medium'] = fuzz.trimf(var.universe, [30, 50, 70])
    var['high'] = fuzz.trimf(var.universe, [55, 100, 100])

combine['few'] = fuzz.trimf(combine.universe, [1, 1, 4])
combine['some'] = fuzz.trimf(combine.universe, [3, 5, 7])
combine['many'] = fuzz.trimf(combine.universe, [6, 10, 10])

priority['low'] = fuzz.trimf(priority.universe, [0, 0, 40])
priority['medium'] = fuzz.trimf(priority.universe, [30, 50, 70])
priority['high'] = fuzz.trimf(priority.universe, [60, 100, 100])

r1 = ctrl.Rule(density['high'] & load['low'] & traffic['low'], combine['many'])
r2 = ctrl.Rule(density['medium'] & traffic['high'] & urgency['medium'], combine['few'])
r3 = ctrl.Rule(load['high'] & density['high'] & profit['medium'], combine['some'])
r4 = ctrl.Rule(density['low'] & urgency['high'] & traffic['medium'], combine['few'])
r5 = ctrl.Rule(profit['high'] & urgency['high'] & traffic['high'], combine['few'])

r6 = ctrl.Rule(urgency['high'] & profit['high'], priority['high'])
r7 = ctrl.Rule(urgency['medium'] & traffic['medium'], priority['medium'])
r8 = ctrl.Rule(urgency['low'] & density['high'] & profit['low'], priority['low'])

delivery_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8])
delivery_sim = ctrl.ControlSystemSimulation(delivery_ctrl)

delivery_sim.input['density'] = 85
delivery_sim.input['urgency'] = 50
delivery_sim.input['load'] = 15
delivery_sim.input['traffic'] = 50
delivery_sim.input['profit'] = 50

delivery_sim.compute()

print(f"Số lượng đơn nên gộp (1-10): {delivery_sim.output['combine']:.1f} đơn")
print(f"Điểm ưu tiên giao hàng (0-100): {delivery_sim.output['priority']:.1f}")