"""
Práctica 2: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nayeli Bonilla Martinez
Número de control: 22212381
Correo institucional: l22212381@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
# Respuesta del sistema en lazo abierto y en lazo cerrado

import numpy as np 
import control as ctrl 
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Datos generales de la simulacion 
u = np.array(pd.read_excel('signal.xlsx', header=None))
x0, t0, tend, dt, w, h = 0, 0, 15, 1E-3, 10, 5
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)
u = np.reshape(signal.resample(u, len(t)), -1)

# Función de transferencia corregida y estable (basada en el modelo RLC correcto)
def cardio(Z, L, R, C):
    num = [L * R, R * Z]
    den = [C * L * R * Z, L * (Z + R), R * Z]  # Denominador estable
    sys = ctrl.tf(num, den)
    polos = np.roots(den)
    return sys, polos

# Funcion de transferencia: Hipotenso
Z, L, R, C = 0.010, 0.001, 1.00, 3.500
syshipo, L_hipo = cardio(Z, L, R, C)
print(f'Funcion de transferencia del hipotenso (caso 1): {syshipo}')
print(f"Polos del sistema: L1 = {L_hipo[0]:.3e}, L2 = {L_hipo[1]:.3e}\n")

# Funcion de transferencia: Normotenso
Z, L, R, C = 0.010, 0.001, 1.00, 1.500
sysnormo, L_normo = cardio(Z, L, R, C)
print(f'Funcion de transferencia del Normotenso (control): {sysnormo}')
print(f"Polos del sistema: L1 = {L_normo[0]:.3e}, L2 = {L_normo[1]:.3e}\n")

# Funcion de transferencia: Hipertenso
Z, L, R, C = 0.010, 0.001, 1.00, 1.000
syshiper, L_hiper = cardio(Z, L, R, C)
print(f'Funcion de transferencia del hipertenso (caso 2): {syshiper}')
print(f"Polos del sistema: L1 = {L_hiper[0]:.3e}, L2 = {L_hiper[1]:.3e}\n")

# Respuesta en lazo abierto
_, PpN = ctrl.forced_response(sysnormo, t, u, x0)
_, PpL = ctrl.forced_response(syshipo, t, PpN, x0)
_, PpH = ctrl.forced_response(syshiper, t, PpN, x0)

# Colores
clr1 = np.array([80, 3, 192]) / 255
clr2 = np.array([171, 3, 169]) / 255
clr3 = np.array([255, 213, 30]) / 255
clr4 = np.array([3, 252, 232]) / 255

# --- Figura 1: Lazo abierto ---
fg1 = plt.figure(1)
fg1.set_size_inches(w, h)
plt.plot(t, PpL, '--', linewidth=0.5, color=clr1, label='Pp(t) Hipotenso')
plt.plot(t, PpN, '-', linewidth=0.5, color=clr2, label='Pp(t) Normotenso')
plt.plot(t, PpH, ':', linewidth=0.5, color=clr3, label='Pp(t) Hipertenso')
plt.xlim(0, 15); plt.xticks(np.arange(0, 16, 1))
plt.ylim(-0.4, 1.2); plt.yticks(np.arange(-0.4, 1.4, 0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', ncol=3, frameon=False)
plt.show()
fg1.savefig('Individuos_python.pdf', bbox_inches='tight')

# Controlador PID
def controlador(kP, kI, kD, sys):
    Cr = 1e-6
    Re = 1 / (kI * Cr)
    Rr = kP * Re
    Ce = kD / Rr
    numPID = [Re * Rr * Ce * Cr, Re * Ce + Rr * Cr]
    denPID = [Re * Cr, 0]
    PID = ctrl.tf(numPID, denPID)
    sysPID = ctrl.feedback(ctrl.series(PID, sys), 1, sign=-1)
    return sysPID

hipoPID = controlador(462.94432652274, 1133845.892515, 0.0062678328455141, syshipo)
print(f"Funcion de transferencia del hipotenso en lazo cerrado: {hipoPID}\n")
hiperPID = controlador(135.230473508502, 338552.543784993, 0.00174865251719904, syshiper)
print(f"Funcion de transferencia del hipertenso en lazo cerrado: {hiperPID}\n")

# Respuesta lazo cerrado
_, PIDL = ctrl.forced_response(hipoPID, t, PpN, x0)
_, PIDH = ctrl.forced_response(hiperPID, t, PpN, x0)

# --- Figura 2: Hipotenso con PID ---
fg2 = plt.figure(2)
fg2.set_size_inches(w, h)
plt.plot(t, PpN, '-', linewidth=0.5, color=clr2, label='Pp(t) Normotenso')
plt.plot(t, PpL, '--', linewidth=0.5, color=clr1, label='Pp(t) Hipotenso')
plt.plot(t, PIDL, ':', linewidth=0.5, color=clr4, label='PID(t) Hipotenso')
plt.xlim(0, 15); plt.xticks(np.arange(0, 16, 1))
plt.ylim(-0.4, 1.2); plt.yticks(np.arange(-0.4, 1.4, 0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', ncol=3, frameon=False)
plt.show()
fg2.savefig('Hipotenso_python.pdf', bbox_inches='tight')

# --- Figura 3: Hipertenso con PID ---
fg3 = plt.figure(3)
fg3.set_size_inches(w, h)
plt.plot(t, PpN, '-', linewidth=0.5, color=clr2, label='Pp(t) Normotenso')
plt.plot(t, PpH, '--', linewidth=0.5, color=clr3, label='Pp(t) Hipertenso')
plt.plot(t, PIDH, ':', linewidth=0.5, color=clr4, label='PID(t) Hipertenso')
plt.xlim(0, 15); plt.xticks(np.arange(0, 16, 1))
plt.ylim(-0.4, 1.2); plt.yticks(np.arange(-0.4, 1.4, 0.2))
plt.xlabel('t [s]')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', ncol=3, frameon=False)
plt.show()
fg3.savefig('Hipertenso_python.pdf', bbox_inches='tight')