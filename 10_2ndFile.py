import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Визначаємо рівняння для системи Базикіна
def bazikin_system(N, t, A, B, beta, E, C, D, M):
    N1, N2 = N
    dN1_dt = A * N1 - (B * N1 * N2) / (1 + beta * N1) - E * N1**2
    dN2_dt = -C * N2 + (D * N1 * N2) / (1 + beta * N1) - M * N2**2
    return [dN1_dt, dN2_dt]

# Параметри моделі
A, B, beta, E, C, D, M = 0.7, 0.1, 0.05, 0.1, 0.5, 0.1, 0.1

# Початкові умови
initial_populations = [10, 5]

# Часові точки
t_points = np.linspace(0, 100, 1000)

# Розв'язок системи
solutions = odeint(bazikin_system, initial_populations, t_points, args=(A, B, beta, E, C, D, M))

# Область для streamplot
X, Y = np.meshgrid(np.linspace(0, max(solutions[:,0])*1.1, 20), np.linspace(0, max(solutions[:,1])*1.1, 20))
U, V = np.zeros(X.shape), np.zeros(Y.shape)
NI, NJ = X.shape

for i in range(NI):
    for j in range(NJ):
        xdot = bazikin_system([X[i, j], Y[i, j]], 0, A, B, beta, E, C, D, M)
        U[i, j] = xdot[0]
        V[i, j] = xdot[1]

# Часова динаміка популяцій
plt.figure(figsize=(10, 5))
plt.plot(t_points, solutions[:, 0], label='Популяція виду $N_1$')
plt.plot(t_points, solutions[:, 1], label='Популяція виду $N_2$')
plt.title('Часова динаміка популяцій')
plt.xlabel('Час')
plt.ylabel('Розмір популяції')
plt.legend()
plt.grid(True)
plt.savefig('Time_Dynamics.png')
plt.show()

# Фазовий портрет без стрілок
plt.figure(figsize=(8, 6))
plt.plot(solutions[:, 0], solutions[:, 1])
plt.title('Фазовий портрет')
plt.xlabel('Популяція виду $N_1$')
plt.ylabel('Популяція виду $N_2$')
plt.grid(True)
plt.savefig('Phase_Portrait_No_Arrows.png')
plt.show()

# Фазовий портрет зі стрілками
plt.figure(figsize=(8, 6))
plt.streamplot(X, Y, U, V, density=1.5)
plt.plot(solutions[:, 0], solutions[:, 1], 'r-')  # Додаємо траєкторію
plt.title('Фазовий портрет зі стрілками')
plt.xlabel('Популяція виду $N_1$')
plt.ylabel('Популяція виду $N_2$')
plt.grid(True)
plt.show()

# Вивід інформації про популяції
start_pop = solutions[0]
mid_pop = solutions[len(solutions)//2]
end_pop = solutions[-1]

print("Початкові розміри популяцій: Вид 1 =", start_pop[0], "Вид 2 =", start_pop[1])
print("Розміри популяцій у середині симуляції: Вид 1 =", mid_pop[0], "Вид 2 =", mid_pop[1])
print("Розміри популяцій на кінці симуляції: Вид 1 =", end_pop[0], "Вид 2 =", end_pop[1])
