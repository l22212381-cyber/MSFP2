[![Open in MATLAB Online](https://www.mathworks.com/images/responsive/global/open-in-matlab-online.svg)](https://matlab.mathworks.com/)

# Práctica 2 — Modelado y control del sistema cardiovascular mediante el modelo Windkessel

Repositorio académico de la asignatura **Modelado de Sistemas Fisiológicos**, del programa de **Ingeniería Biomédica** del Tecnológico Nacional de México / Instituto Tecnológico de Tijuana.

Esta práctica estudia el comportamiento dinámico del sistema cardiovascular mediante el **modelo Windkessel de cuatro elementos**. Se comparan tres condiciones simuladas —hipotensa, normotensa e hipertensa— y se toma la respuesta normotensa como referencia para diseñar controladores PID que reduzcan las diferencias entre la respuesta de referencia y las respuestas de los otros dos casos.

**Docente:** Dr. Paul Antonio Valle Trujillo  
**Correo:** paul.valle@tectijuana.edu.mx  
**Departamento:** Ingeniería Eléctrica y Electrónica  
**Institución:** Tecnológico Nacional de México / Instituto Tecnológico de Tijuana  
**Asignatura:** Modelado de Sistemas Fisiológicos  
**Programa:** Ingeniería Biomédica  
**Estudiante(s):** Nombre completo · Número de control · correo institucional  

**Repositorio de la asignatura:** https://github.com/DrPaulValle/MSF-IBF1020  
**Modalidad de la práctica:** simulación *in silico*. Los controladores se desarrollan con fines académicos; no representan tratamientos médicos ni recomendaciones clínicas.

---

## Contenido

1. [Resumen](#resumen)
2. [Competencia y objetivos](#objetivos)
3. [Descripción del modelo Windkessel](#modelo)
4. [Parámetros de los individuos](#parametros)
5. [Formulación matemática](#matematico)
6. [Análisis de estabilidad y estado estacionario](#estabilidad)
7. [Simulación en MATLAB, Simulink y Simscape](#matlab)
8. [Diseño de controladores PID](#pid)
9. [Implementación en Python](#python)
10. [Resultados y verificación cruzada](#resultados)
11. [Diagrama biológico](#diagrama)
12. [Estructura del repositorio](#estructura)
13. [Requisitos y reproducción](#reproducibilidad)
14. [Conclusiones](#conclusiones)
15. [Referencias](#referencias)

---

<a id="resumen"></a>
## 1. Resumen

El modelo Windkessel representa propiedades fundamentales de la dinámica arterial mediante elementos eléctricos equivalentes. En esta práctica se utiliza un modelo de cuatro elementos: impedancia característica \(Z\), distensibilidad arterial \(C\), resistencia periférica \(R\) e inertancia arterial \(L\). La presión se representa mediante voltaje y el flujo sanguíneo mediante corriente.

Se analizan tres conjuntos de parámetros: hipotenso, normotenso e hipertenso. El caso normotenso funciona como referencia, mientras que los otros dos casos se estudian primero en lazo abierto y posteriormente en lazo cerrado. Se construyen representaciones mediante ecuaciones de estado, funciones de transferencia y un circuito equivalente en Simscape Electrical. Además, se implementan las funciones de transferencia en Python para comparar sus respuestas con las obtenidas en MATLAB/Simulink.

**Palabras clave:** modelo Windkessel; sistema cardiovascular; presión arterial; distensibilidad arterial; ecuaciones de estado; función de transferencia; estabilidad; PID; MATLAB; Simulink; Simscape Electrical; Python.

[Volver al contenido](#contenido)

---

<a id="objetivos"></a>
## 2. Competencia y objetivos

### Competencia a desarrollar

Modelizar sistemas fisiológicos mediante circuitos eléctricos equivalentes, ecuaciones diferenciales y funciones de transferencia para analizar su comportamiento dinámico, y diseñar estrategias de control mediante técnicas de control clásico.

### Objetivo general

Analizar y comparar el comportamiento dinámico de los modelos cardiovasculares hipotenso e hipertenso respecto a un modelo normotenso de referencia, mediante la formulación matemática, simulación computacional y diseño de controladores PID en un entorno *in silico*.

### Objetivos específicos

- Identificar las variables de entrada, salida, estados y parámetros del modelo Windkessel.
- Relacionar los elementos \(Z\), \(C\), \(R\) y \(L\) con las propiedades hemodinámicas que representan.
- Obtener las ecuaciones de estado y las funciones de transferencia de los tres conjuntos de parámetros.
- Analizar el error en estado estacionario, los polos y la estabilidad de cada modelo.
- Comparar las respuestas en lazo abierto ante la misma señal de excitación.
- Diseñar dos controladores PID independientes: uno para el caso hipotenso y otro para el hipertenso, ambos con referencia normotensa.
- Implementar y comparar los modelos en MATLAB/Simulink, Simscape Electrical y Python.
- Documentar los parámetros, ganancias, figuras, diagramas y resultados en GitHub.

[Volver al contenido](#contenido)

---

<a id="modelo"></a>
## 3. Descripción del modelo Windkessel

El modelo Windkessel de cuatro elementos aproxima la dinámica del sistema arterial usando componentes equivalentes a propiedades hemodinámicas:

| Elemento | Interpretación en el modelo |
|---|---|
| \(Z\) | Impedancia característica de la región proximal del sistema arterial |
| \(C\) | Distensibilidad arterial total |
| \(R\) | Resistencia periférica |
| \(L\) | Inertancia asociada con la masa de sangre en movimiento |

La analogía eléctrica empleada establece que la **presión arterial corresponde al voltaje** y el **flujo sanguíneo corresponde a la corriente**. La capacitancia \(C\) y la inertancia \(L\) son los dos elementos independientes de almacenamiento de energía, por lo que el sistema puede describirse como un modelo dinámico de segundo orden.

Las variables principales que deben identificarse en el circuito son la presión de entrada \(P_a(t)\), la presión sobre la distensibilidad \(P_p(t)\), el flujo de entrada \(F_a(t)\) y el flujo a través de la inertancia \(F_L(t)\). Se debe conservar la notación utilizada en el desarrollo matemático y en los modelos entregados por la asignatura.

[Volver al contenido](#contenido)

---

<a id="parametros"></a>
## 4. Parámetros de los individuos

Los tres modelos mantienen constantes \(Z\), \(L\) y \(R\); la distensibilidad arterial \(C\) es el parámetro que cambia entre los casos.

| Parámetro | Hipotenso | Normotenso | Hipertenso | Unidades indicadas en la práctica |
|---|---:|---:|---:|---|
| \(Z\) | 0.010 | 0.010 | 0.010 | mmHg·s·ml⁻¹ |
| \(L\) | 0.001 | 0.001 | 0.001 | mmHg·s²·ml⁻¹ |
| \(R\) | 1.000 | 1.000 | 1.000 | mmHg·s·ml⁻¹ |
| \(C\) | 3.500 | 1.500 | 1.000 | ml·mmHg⁻¹ |

En el modelo de la práctica, el caso hipotenso tiene una distensibilidad mayor, mientras que el caso hipertenso presenta una distensibilidad menor. El **modelo normotenso se utiliza como referencia** para evaluar la diferencia entre respuestas.

[Volver al contenido](#contenido)

---

<a id="matematico"></a>
## 5. Formulación matemática

### 5.1 Variables de estado

El modelo se formula mediante dos variables de estado:

\[
x_1(t)=F_L(t), \qquad x_2(t)=P_p(t)
\]

La presión arterial de entrada se considera como la entrada del sistema:

\[
u(t)=P_a(t)
\]

La salida considerada es la presión sobre la distensibilidad arterial:

\[
y(t)=P_p(t)
\]

### 5.2 Ecuaciones de estado

A partir de las relaciones del circuito Windkessel y las leyes de Kirchhoff, se construye el modelo en la forma:

\[
\dot{x}(t)=Ax(t)+Bu(t), \qquad y(t)=Cx(t)+Du(t)
\]

En la entrega deben incluirse las matrices \(A\), \(B\), \(C\) y \(D\) obtenidas durante el desarrollo, así como la explicación de las relaciones físicas que representa cada ecuación. Verificar que las matrices y la salida coincidan con el modelo implementado en MATLAB/Simulink y Python.

### 5.3 Funciones de transferencia

Con condiciones iniciales nulas, se obtiene la función de transferencia entre la presión arterial de entrada y la presión sobre la distensibilidad:

\[
G(s)=\frac{P_p(s)}{P_a(s)}
\]

Se deben documentar las tres funciones correspondientes a los parámetros de la práctica:

- \(G_{\mathrm{hipo}}(s)\): modelo hipotenso.
- \(G_{\mathrm{normo}}(s)\): modelo normotenso.
- \(G_{\mathrm{hiper}}(s)\): modelo hipertenso.

**Importante:** incorporar aquí las expresiones finales derivadas y verificadas en el cuaderno de MATLAB o en el desarrollo matemático. No deben copiarse funciones de transferencia sin comprobar sus coeficientes y la correspondencia con los parámetros.

[Volver al contenido](#contenido)

---

<a id="estabilidad"></a>
## 6. Análisis de estabilidad y estado estacionario

Para cada función de transferencia se deben realizar las siguientes comprobaciones:

1. **Respuesta al escalón:** determinar la respuesta final y calcular el error en estado estacionario.
2. **Polos:** obtener los polos de \(G_{\mathrm{hipo}}(s)\), \(G_{\mathrm{normo}}(s)\) y \(G_{\mathrm{hiper}}(s)\).
3. **Estabilidad:** representar los polos en el plano complejo y analizar sus partes reales.
4. **Comparación dinámica:** relacionar los cambios en la distensibilidad \(C\) con las diferencias observadas en la respuesta temporal.

Agregar al repositorio los cálculos, las gráficas de polos y una breve interpretación de los resultados de cada caso. Las conclusiones deben basarse en los valores obtenidos al ejecutar los modelos.

[Volver al contenido](#contenido)

---

<a id="matlab"></a>
## 7. Simulación en MATLAB, Simulink y Simscape

La práctica solicita tres representaciones para las condiciones hipotensa, normotensa e hipertensa:

| Representación | Propósito |
|---|---|
| Ecuaciones de estado en Simulink | Verificar la dinámica a partir de las variables de estado |
| Función de transferencia en Simulink | Analizar la relación entrada-salida |
| Circuito equivalente en Simscape Electrical | Representar los componentes eléctricos del modelo Windkessel |

### Señal de excitación

Se utiliza el bloque **Uniform Random Number** con los parámetros indicados en el documento de la práctica:

- Mínimo: \(-0.2\)
- Máximo: \(1\)
- Semilla (*seed*): \(106\)
- Tiempo de muestreo: \(T_s=0.18\ \mathrm{s}\)
- Intervalo de simulación: \(0\leq t\leq15\ \mathrm{s}\)

Debe utilizarse exactamente la misma realización de la señal aleatoria para los tres modelos, de modo que las diferencias de las respuestas se deban a los parámetros y no a entradas distintas.

[Volver al contenido](#contenido)

---

<a id="pid"></a>
## 8. Diseño de controladores PID

La respuesta del modelo normotenso se utiliza como referencia. Se implementan dos sistemas de retroalimentación independientes:

1. **Normotenso–hipotenso:** se compara la respuesta normotensa con la respuesta hipotensa.
2. **Normotenso–hipertenso:** se compara la respuesta normotensa con la respuesta hipertensa.

Los errores de seguimiento se definen como:

\[
e_{\mathrm{hipo}}(t)=P_{p,\mathrm{normo}}(t)-P_{p,\mathrm{hipo}}(t)
\]

\[
e_{\mathrm{hiper}}(t)=P_{p,\mathrm{normo}}(t)-P_{p,\mathrm{hiper}}(t)
\]

Para cada sistema se agrega un bloque **PID Controller** y se utiliza la herramienta **Tune** de Simulink para obtener las ganancias \(K_P\), \(K_I\) y \(K_D\). Las ganancias deben registrarse por separado, junto con capturas de la configuración y de las respuestas obtenidas.

| Controlador | Ganancias por documentar |
|---|---|
| Caso hipotenso | \(K_{P,\mathrm{hipo}}\), \(K_{I,\mathrm{hipo}}\), \(K_{D,\mathrm{hipo}}\) |
| Caso hipertenso | \(K_{P,\mathrm{hiper}}\), \(K_{I,\mathrm{hiper}}\), \(K_{D,\mathrm{hiper}}\) |

El propósito de la sintonización es obtener una respuesta estable y reducir el error entre cada caso y la referencia normotensa. No se deben inventar ganancias: incluir los valores reales obtenidos durante la simulación.

[Volver al contenido](#contenido)

---

<a id="python"></a>
## 9. Implementación en Python

El archivo `Bonilla22212381.py` permite implementar las funciones de transferencia de los modelos hipotenso, normotenso e hipertenso. La implementación debe reproducir la misma señal de entrada utilizada en MATLAB/Simulink y realizar las siguientes tareas:

- Definir los parámetros de los tres modelos.
- Construir las funciones de transferencia.
- Simular las respuestas en lazo abierto.
- Incorporar las ganancias PID obtenidas mediante la herramienta Tune.
- Construir los sistemas hipotenso y hipertenso en lazo cerrado.
- Graficar y guardar las respuestas para compararlas con MATLAB/Simulink.

Para una comparación válida, utilizar los mismos parámetros, la misma entrada, el mismo intervalo temporal y las mismas ganancias. Documentar cualquier diferencia atribuible al método numérico o a la implementación.

[Volver al contenido](#contenido)

---

<a id="resultados"></a>
## 10. Resultados y verificación cruzada

Los resultados deben permitir comparar las respuestas de los tres modelos en lazo abierto y evaluar el efecto de los controladores en los casos hipotenso e hipertenso.

### Comparaciones requeridas

- Respuestas hipotensa, normotensa e hipertensa en lazo abierto.
- Respuesta de referencia normotensa frente al caso hipotenso antes y después del control.
- Respuesta de referencia normotensa frente al caso hipertenso antes y después del control.
- Comparación entre ecuaciones de estado, funciones de transferencia y circuito de Simscape Electrical.
- Comparación de las figuras generadas en MATLAB/Simulink con las obtenidas en Python.

### Evidencias

Insertar o enlazar las figuras generadas y describir qué muestran. Para cada comparación, indicar las variables y sus unidades, identificar la señal de referencia y explicar si el controlador reduce el error. Registrar las ganancias PID reales y señalar cualquier diferencia entre plataformas.

Los resultados numéricos, las figuras y las conclusiones deben completarse con las salidas reales del programa. Este README no presupone resultados que no se hayan calculado.

[Volver al contenido](#contenido)

---

<a id="diagrama"></a>
## 11. Diagrama biológico

La práctica solicita elaborar un diagrama del sistema cardiovascular con BioRender o una herramienta equivalente. El diagrama debe identificar, como mínimo:

- Corazón.
- Aorta y grandes arterias.
- Vasos periféricos.
- Flujo sanguíneo.
- Presión arterial.
- Distensibilidad arterial.
- Resistencia periférica.

Relacionar los elementos anatómicos y fisiológicos con los parámetros \(Z\), \(C\), \(R\) y \(L\) del modelo Windkessel. Guardar el diagrama en el repositorio y explicar brevemente la correspondencia entre el sistema fisiológico y su representación matemática.

[Volver al contenido](#contenido)

---

<a id="estructura"></a>
## 12. Estructura del repositorio

La siguiente lista refleja los archivos reportados para la práctica. Se recomienda conservar los nombres reales y organizar las evidencias de forma que las rutas de este README coincidan con los archivos subidos a GitHub.

```text
.
├── README.md
├── LICENSE
├── Análisis matemático.pdf
├── Bonilla22212381.mlx
├── Bonilla22212381.pdf
├── Bonilla22212381.py
├── Sistemab.slx
├── Sistema Cardiovascular.jpeg
├── signal.xlsx
├── Hipertenso_python.pdf
├── Hipotenso_python.pdf
├── hipertenso_matlab.pdf
├── hipotenso_matlab.pdf
├── individuos_matlab.pdf
├── individuos_python.pdf
├── odes_matlab.pdf
├── Parametros del controlador Hipertenso.pdf
└── Parametros del controlador Hipotenso.pdf
```

**Descripción general de los archivos:**

| Archivo | Contenido / propósito |
|---|---|
| `README.md` | Reporte y guía de reproducción de la práctica |
| `Análisis matemático.pdf` | Desarrollo o documentación del análisis matemático |
| `Bonilla22212381.mlx` | Cuaderno computacional de MATLAB |
| `Bonilla22212381.pdf` | Exportación en PDF del cuaderno de MATLAB |
| `Bonilla22212381.py` | Implementación del modelo en Python |
| `Sistemab.slx` | Modelo de Simulink |
| `Sistema Cardiovascular.jpeg` | Imagen del sistema cardiovascular |
| `signal.xlsx` | Archivo de señal utilizado por el código, según la configuración de la práctica |
| `Hipertenso_python.pdf`, `Hipotenso_python.pdf` | Resultados asociados a los modelos en Python |
| `hipertenso_matlab.pdf`, `hipotenso_matlab.pdf` | Resultados asociados a los modelos en MATLAB |
| `individuos_matlab.pdf`, `individuos_python.pdf` | Comparaciones de los individuos por plataforma |
| `odes_matlab.pdf` | Resultados de la representación mediante ecuaciones diferenciales en MATLAB |
| `Parametros del controlador Hipertenso.pdf`, `Parametros del controlador Hipotenso.pdf` | Parámetros registrados para los controladores de ambos casos |
| `LICENSE` | Licencia del repositorio |

Si se agregan capturas, figuras o carpetas adicionales, actualizar esta sección para que refleje la estructura final de GitHub.

[Volver al contenido](#contenido)

---

<a id="reproducibilidad"></a>
## 13. Requisitos y reproducción

### Software

- MATLAB.
- Simulink.
- Simscape Electrical.
- Python y Visual Studio Code.
- Las bibliotecas importadas por el archivo `Bonilla22212381.py`.
- Git y GitHub.

### Secuencia recomendada

1. Revisar el desarrollo matemático y la tabla de parámetros.
2. Verificar las ecuaciones de estado y las funciones de transferencia.
3. Ejecutar los modelos en Simulink y Simscape Electrical para los tres conjuntos de parámetros.
4. Confirmar que se utiliza la misma señal aleatoria en los tres casos.
5. Comparar las respuestas en lazo abierto.
6. Construir los dos sistemas de control tomando el modelo normotenso como referencia.
7. Sintonizar los controladores PID con Tune y registrar sus ganancias.
8. Ejecutar el cuaderno MATLAB y exportar las gráficas.
9. Ejecutar el programa Python con la misma entrada y las mismas ganancias.
10. Comparar los resultados entre las distintas representaciones y plataformas.
11. Incorporar las figuras, capturas, el diagrama biológico y las conclusiones.
12. Revisar que todos los archivos mencionados en el README estén incluidos en el repositorio.

[Volver al contenido](#contenido)

---

<a id="conclusiones"></a>
## 14. Conclusiones

Completar esta sección después de analizar los resultados obtenidos. Las conclusiones deben abordar:

- Cómo influye la distensibilidad arterial \(C\) en las diferencias entre los modelos hipotenso, normotenso e hipertenso.
- Qué se observó en el análisis de los polos, la estabilidad y la respuesta al escalón.
- En qué medida los controladores PID redujeron el error respecto a la referencia normotensa.
- Qué tan consistentes fueron los resultados de MATLAB/Simulink, Simscape Electrical y Python.
- Qué diferencias o limitaciones se observaron durante la simulación.

Las conclusiones deben describir los resultados de esta práctica académica y no deben interpretarse como recomendaciones de diagnóstico o tratamiento.

[Volver al contenido](#contenido)

---

<a id="referencias"></a>
## 15. Referencias

1. Valle Trujillo, P. A. (2026). *Modelado de Sistemas Fisiológicos: Práctica 2, Modelado y control del sistema cardiovascular mediante el modelo Windkessel*. Tecnológico Nacional de México / Instituto Tecnológico de Tijuana. Material de práctica proporcionado en la asignatura.
2. Frank, O. (referencia histórica del modelo Windkessel mencionada en el material de la práctica). Completar los datos bibliográficos si se consulta una fuente primaria o secundaria específica.
3. Agregar aquí los libros, artículos o documentación técnica consultados para fundamentar el modelo, la fisiología cardiovascular y las herramientas de simulación.

[Volver al contenido](#contenido)

---

## Uso académico

Este repositorio documenta una práctica de **Modelado de Sistemas Fisiológicos** desarrollada mediante simulación *in silico*. Deben distinguirse los parámetros y resultados proporcionados por la práctica de los resultados calculados por el estudiante, así como de cualquier modificación propia. Los sistemas de control incluidos tienen fines exclusivamente académicos y no constituyen estrategias terapéuticas.
