import numpy as np
import matplotlib.pyplot as plt

# Свойства веревки
length = 1.0  # длина веревки, м
diameter = 0.0006  # диаметр веревки, м
area = np.pi * (diameter / 2) ** 2  # площадь поперечного сечения, м^2
young_modulus = 146.64e6  # модуль упругости, Па (примерное значение для лавсан)
tensile_strength = 172e6  # предел прочности на разрыв, Па (примерное значение для лавсан)

# Эффективность узлов
knot_efficiencies = {
    'Девятка': 0.7,
    'Двойной булинь': 0.53,
    'Проводник': 0.5,
}

# Параметры моделирования
num_segments = 100  # количество сегментов
segment_length = length / num_segments  # длина одного сегмента, м
force_increment = 0.1  # прирост силы на шаг, Н

# Функция для расчета удлинения сегмента
def calculate_elongation(force, length, area, young_modulus):
    stress = force / area  # вычисление напряжения в сегменте
    strain = stress / young_modulus  # вычисление деформации в сегменте
    elongation = strain * length  # вычисление удлинения сегмента
    return elongation

# Функция для моделирования с узлом
def simulate_knot(knot_name, knot_efficiency):
    forces = np.zeros(num_segments)  # массив сил в каждом сегменте веревки
    displacements = np.zeros(num_segments + 1)  # массив удлинений в каждом узле веревки

    # Массив для записи силы и удлинения
    force_values = [0]
    elongation_values = [0]

    adjusted_tensile_strength = tensile_strength * knot_efficiency

    breaking_force = None
    max_elongation = 0
    for step in range(10000):
        forces[-1] += force_increment  # увеличение силы на конце веревки на каждом шаге
        for i in range(num_segments):
            force = forces[i]  # сила в текущем сегменте
            elongation = calculate_elongation(force, segment_length, area, young_modulus)  # расчет удлинения сегмента
            displacements[i + 1] = displacements[i] + elongation  # обновление удлинения узла

        total_elongation = displacements[-1]  # общее удлинение веревки
        force_values.append(forces[-1])  # запись текущей силы в массив
        elongation_values.append(total_elongation)  # запись текущего удлинения в массив

        # Проверка на разрыв
        if forces[-1] / area > adjusted_tensile_strength:
            breaking_force = forces[-1]
            max_elongation = total_elongation
            break

    # Вывод результатов
    print(f'{knot_name}: Пороговое значение силы разрыва: {breaking_force} Н')
    print(f'{knot_name}: Максимальное удлинение до разрыва: {max_elongation} м')

    return force_values, elongation_values, breaking_force, max_elongation

# Моделирование без узла
force_values_no_knot, elongation_values_no_knot, breaking_force_no_knot, max_elongation_no_knot = simulate_knot('Без узла', 1.0)

# Моделирование для каждого типа узла
plt.figure(figsize=(15, 8))

# График без узла
plt.subplot(2, 3, 1)
plt.plot(force_values_no_knot, elongation_values_no_knot, label='Удлинение нити/Сила')
plt.xlabel('Сила (Н)')
plt.ylabel('Удлинение (м)')
plt.title('Без узла')
plt.axvline(breaking_force_no_knot, color='r', linestyle='--', label='Сила разрыва')
plt.legend()
plt.grid(True)
plt.xlim(0, max(force_values_no_knot)*1.05)
plt.ylim(0, max(elongation_values_no_knot)*1.05)
plt.plot(breaking_force_no_knot, max_elongation_no_knot, 'ko')
plt.text(breaking_force_no_knot, max_elongation_no_knot, f'({breaking_force_no_knot:.1f} Н, {max_elongation_no_knot:.4f} м)', verticalalignment='bottom', horizontalalignment='right', color='black')

# Графики с узлами
for idx, (knot_name, knot_efficiency) in enumerate(knot_efficiencies.items(), 2):
    force_values, elongation_values, breaking_force, max_elongation = simulate_knot(knot_name, knot_efficiency)
    plt.subplot(2, 3, idx+2)
    plt.plot(force_values, elongation_values, label='Удлинение нити/Сила')
    plt.xlabel('Сила (Н)')
    plt.ylabel('Удлинение (м)')
    plt.title(knot_name)
    plt.axvline(breaking_force, color='r', linestyle='--', label='Сила разрыва')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, max(force_values)*1.05)
    plt.ylim(0, max(elongation_values)*1.05)
    plt.plot(breaking_force, max_elongation, 'ko')
    plt.text(breaking_force, max_elongation, f'({breaking_force:.1f} Н, {max_elongation:.4f} м)', verticalalignment='bottom', horizontalalignment='right', color='black')

plt.tight_layout()
plt.show()