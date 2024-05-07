import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fsolve

# Визначаємо диференціальне рівняння для зростання популяції
def population_model(N, t, beta, delta, p):
    return beta * N**2 / (1 + N) - delta * N - p * N**2

# Коефіцієнти, задані в завданні
beta = 16.2  # коефіцієнт народжуваності
delta = 2.1  # коефіцієнт смертності
p = 6        # внутрішньовидова конкуренція

# Визначення критичних меж чисельності популяції
def equilibrium(N):
    return beta * N**2 / (1 + N) - delta * N - p * N**2

initial_guesses = [0.1, 1, 10]
equilibria = [fsolve(equilibrium, x0)[0] for x0 in initial_guesses if fsolve(equilibrium, x0)[0] > 0]
lower_critical_limit, upper_critical_limit = np.sort(np.unique(equilibria))

# Точки часу для симуляції
t = np.linspace(0, 50, 500)

# Визначення початкових умов на основі вимог завдання
initial_conditions = {
    'a': lower_critical_limit / 2 * 0.99,
    'b': lower_critical_limit / 2 * 1.01,
    'c': lower_critical_limit,
    'd1': (upper_critical_limit + lower_critical_limit) / 4,
    'd2': (3 * upper_critical_limit + lower_critical_limit) / 4,
    'e': upper_critical_limit,
    'f': upper_critical_limit * 1.01
}

# Розв'язання диференціального рівняння для кожної початкової умови
solution = {}
for key, N0 in initial_conditions.items():
    solution[key] = odeint(population_model, N0, t, args=(beta, delta, p))

# Малюємо результати для кожного сценарію початкових умов на окремих графіках
plt.figure(figsize=(18, 12))
for idx, (key, sol) in enumerate(solution.items(), 1):
    plt.subplot(4, 2, idx)
    plt.plot(t, sol, label=f'Умова {key}')
    plt.title(f'Динаміка за початковою умовою {key}')
    plt.xlabel('Час')
    plt.ylabel('Розмір популяції (N)')
    plt.legend()
    plt.grid(True)

# Додатковий графік з усіма динаміками на одному малюнку для порівняння
plt.figure(figsize=(12, 8))
for key, sol in solution.items():
    plt.plot(t, sol, label=f'Умова {key}')
plt.title('Загальна динаміка популяції')
plt.xlabel('Час')
plt.ylabel('Розмір популяції (N)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Вивід критичних точок та висновків у консоль
print(f'Нижня критична межа (рівновага): {lower_critical_limit}')
print(f'Верхня критична межа (рівновага): {upper_critical_limit}')
for key, sol in solution.items():
    final_size = sol[-1, 0]
    conclusion = 'стабілізується в точці рівноваги.' if np.isclose(final_size, lower_critical_limit, atol=0.1) or np.isclose(final_size, upper_critical_limit, atol=0.1) else 'не стабілізується в точці рівноваги.'
    print(f'Початкова умова {key}: Популяція {conclusion}')
