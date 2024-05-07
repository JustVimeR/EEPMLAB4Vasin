import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Диференціальне рівняння для зростання популяції пацючків
def rat_population_model(N, t):
    return 0.0008 * N**2 - 0.128 * N

# Розрахунок рівноважного розміру популяції (де dN/dt = 0)
def calculate_equilibrium():
    # 0.0008 * N^2 - 0.128 * N = 0
    # N(0.0008 * N - 0.128) = 0, N = 0 або N = 160
    return 160  # Тільки позитивне, ненульове рівноважне значення

# Початкові умови: 200 пацючків у першому зоопарку, 100 в другому
initial_conditions = {
    'first_zoo': 200,
    'second_zoo': 100
}

# Точки часу для симуляції до 12 місяців
t = np.linspace(0, 12, 300)

# Розв'язуємо диференціальне рівняння для кожної початкової умови
solution = {}
for key in initial_conditions:
    N0 = initial_conditions[key]
    solution[key] = odeint(rat_population_model, N0, t)

# Вивід чисельності пацючків через рік (12 місяців)
for key, sol in solution.items():
    final_population = sol[-1, 0]
    print(f"Чисельність пацючків у {key} через рік: {final_population}")

# Визначення рівноважного розміру популяції
equilibrium = calculate_equilibrium()

# Визначення типу популяції за останньою точкою
for key, sol in solution.items():
    final_population = sol[-1, 0]
    if final_population > equilibrium:
        status = 'перевищує межу ємності.'
    elif final_population < equilibrium:
        status = 'нижче межі ємності.'
    else:
        status = 'стабілізується на межі ємності.'
    print(f"Кінцева популяція для {key} після 12 місяців {status}")

# Малюємо результати для обох зоопарків
plt.figure(figsize=(12, 8))
for key in solution:
    plt.plot(t, solution[key], label=f'Початкова умова: {key}')
    plt.axhline(y=equilibrium, color='red', linestyle='--', label='Рівноважна популяція' if key == 'first_zoo' else None)
plt.title('Динаміка популяції пацючків з плином часу')
plt.xlabel('Час (місяці)')
plt.ylabel('Розмір популяції пацючків (N)')
plt.legend()
plt.grid(True)
plt.show()
