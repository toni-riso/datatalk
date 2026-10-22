# ⚽ DataTalk

Aplicación web progresiva (PWA) para el registro y análisis de eventos de fútbol en tiempo real.

Diseñada para ser utilizada principalmente desde iPad durante partidos de Fútbol 11 o Fútbol 8.

[¡Ver demo cliente!](https://toni-riso.github.io/datatalk/cliente-V2/)

[Plantilla ejemplo F11](cliente/plantilla-F11.txt)

[Plantilla ejemplo F8](cliente/plantilla-F8.txt)

---

# 🚀 Características principales

## Gestión del partido

- Datos del partido
- Fútbol 11 / Fútbol 8
- Cronómetro
- Marcador
- Equipo activo

## Convocatoria

- Alta manual de jugadores
- Importación desde fichero TXT
- Selección de titulares
- Gestión de suplentes
- Eliminación de jugadores

## Gestión de jugadores

- Selección rápida
- Dorsal
- Nombre
- Posición
- Minutos jugados

# 📋 Catálogo de eventos

Data Talk utiliza un modelo de análisis basado en las diferentes fases del juego: **Salida**, **Construcción**, **Finalización**, **Defensa** y **Disciplina**.

---

## ⚽ Salida de balón

### Eventos de equipo

| Evento | Descripción |
|----------|-------------|
| ✅ Salida exitosa | Salida de balón completada con éxito |
| ❌ Salida fallida | Salida de balón perdida o interrumpida |
| ✅ Rival salida exitosa | El rival supera nuestra presión durante su salida de balón |
| ❌ Rival salida fallida | Recuperamos el balón o impedimos que el rival supere la presión |

### Eventos individuales

| Evento | Descripción |
|----------|-------------|
| ❌ Pérdida salida | Pérdida de balón de un jugador durante la fase de salida |

---

## 🔶 Construcción

### Eventos individuales

| Evento | Descripción |
|----------|-------------|
| ✅ Regate | El jugador supera a un adversario manteniendo la posesión |
| ❌ Regate | El jugador intenta superar a un adversario sin éxito |
| ❌ Pérdida construcción | Pérdida de balón durante la fase de construcción del juego |

---

## 🎯 Finalización

### Eventos individuales

| Evento | Descripción |
|----------|-------------|
| 🎯 Tiro fuera | Finalización que no encuentra portería |
| 🥅 Tiro a puerta | Finalización entre los tres palos |
| ⚽ Gol | Gol anotado por un jugador propio |
| ❌ Pérdida finalización | Pérdida de balón durante la fase de finalización |

### Eventos de equipo

| Evento | Descripción |
|----------|-------------|
| 🎯 Rival tiro fuera | Finalización rival fuera de portería |
| 🥅 Rival tiro a puerta | Finalización rival entre los tres palos |
| ⚽ Gol rival | Gol anotado por el equipo contrario |

---

## 🛡️ Acciones defensivas

Las acciones defensivas representan recuperaciones de balón realizadas cuando el equipo no tiene la posesión.

### Eventos individuales

| Evento | Descripción |
|----------|-------------|
| 🔁 Recuperación salida | Recuperación de balón durante la salida rival |
| 🔁 Recuperación construcción | Recuperación de balón durante la construcción rival |
| 🔁 Recuperación finalización | Recuperación de balón durante la finalización rival |

---

## 🟨 Disciplina

### Eventos individuales

| Evento | Descripción |
|----------|-------------|
| 🤕 Falta cometida | Falta realizada por el jugador |
| 🙋 Falta sufrida## Cronología

- Registro automático de eventos
- Línea temporal del partido
- Deshacer último evento

# 📊 Estadísticas generadas por Data Talk

Las estadísticas de Data Talk se calculan a partir de los eventos registrados durante el partido y se organizan siguiendo las diferentes fases del juego:

```text
Salida
↓
Construcción
↓
Finalización
↓
Defensa
↓
Disciplina
```

Esto permite analizar el rendimiento individual de los jugadores y el comportamiento colectivo del equipo de una manera coherente con el modelo de juego.

---

# 👤 Estadísticas individuales

Las estadísticas individuales se calculan únicamente a partir de los eventos asociados directamente a un jugador.

---

## ⏱ Participación

### Minutos jugados

Tiempo efectivo que el jugador ha permanecido en el terreno de juego.

Se calcula a partir de:

```text
stints[]
```

registrados mediante entradas y salidas del campo.

Ejemplo:

```text
Entrada: minuto 0
Salida: minuto 25

Entrada: minuto 35
Salida: minuto 60

Minutos jugados = 50
```

---

## ⭐ Valoración

Valoración automática del jugador en una escala de:

```text
0 → 10
```

La puntuación se genera ponderando:

### Acciones positivas

- Regates exitosos
- Tiros
- Tiros a puerta
- Goles
- Recuperaciones

### Acciones negativas

- Regates fallidos
- Pérdidas
- Faltas cometidas
- Amarillas

Las pérdidas en salida penalizan más que las pérdidas en construcción o finalización debido a su mayor riesgo para el equipo.

---

# ⚽ Salida

## ❌ Pérdidas en salida

Número de balones perdidos durante la fase de salida de balón.

Representa errores en zonas de riesgo alto próximas a la propia portería.

```text
Evento:
loss_buildout
```

---

# 🔶 Construcción

## ✅ Regates exitosos

Acciones en las que el jugador supera a un adversario manteniendo la posesión.

```text
Evento:
dribble_ok
```

---

## ❌ Regates fallidos

Intentos fallidos de superar a un adversario.

```text
Evento:
dribble_bad
```

---

## ❌ Pérdidas en construcción

Número de posesiones perdidas durante la fase de elaboración del juego.

```text
Evento:
loss_build
```

---

# 🎯 Finalización

## 🎯 Tiros fuera

Intentos de finalización que no terminan entre los tres palos.

```text
Evento:
shot_off
```

---

## 🥅 Tiros a puerta

Intentos de finalización entre los tres palos.

```text
Evento:
shot_target
```

---

## ⚽ Goles

Número total de goles anotados por el jugador.

```text
Evento:
goal_own
```

---

## ❌ Pérdidas en finalización

Posesiones perdidas durante la fase de finalización.

```text
Evento:
loss_finish
```

---

# 🛡️ Defensa

## 🔁 Recuperaciones en salida

Recuperaciones de balón realizadas durante la salida rival.

```text
Evento:
recovery_buildout
```

---

## 🔁 Recuperaciones en construcción

Recuperaciones producidas durante la fase de construcción rival.

```text
Evento:
recovery_build
```

---

## 🔁 Recuperaciones en finalización

Recuperaciones realizadas durante la fase de finalización rival.

```text
Evento:
recovery_finish
```

---

# 🟨 Disciplina

## 🤕 Faltas cometidas

Número de faltas realizadas por el jugador.

```text
Evento:
foul_committed
```

---

## 🙋 Faltas sufridas

Número de faltas recibidas por el jugador.

```text
Evento:
foul_received
```

---

## 🟨 Amarillas

Tarjetas amarillas recibidas.

```text
Evento:
yellow
```

---

# 👥 Estadísticas colectivas

Las estadísticas colectivas se generan utilizando todos los eventos registrados durante el partido.

Incluyen tanto los eventos individuales como los eventos colectivos.

---

# ⚽ Salida

## ✅ Salidas exitosas

Número de salidas de balón completadas con éxito por el equipo.

```text
Evento:
buildout_success
```

---

## ❌ Salidas fallidas

Número de salidas de balón que terminan en pérdida o sin superar la presión rival.

```text
Evento:
buildout_fail
```

---

## 📈 Porcentaje de salida

Mide la eficacia del equipo durante la salida de balón.

Fórmula:

```text
Salidas exitosas
────────────────────────────── × 100
Salidas exitosas + Salidas fallidas
```

---

## ✅ Rival salida exitosa

Número de ocasiones en las que el rival consigue superar nuestra presión durante su salida.

```text
Evento:
rival_buildout_success
```

---

## ❌ Rival salida fallida

Número de ocasiones en las que recuperamos el balón o impedimos que el rival supere nuestra presión.

```text
Evento:
rival_buildout_fail
```

---

## 📈 Efectividad de la presión

Mide la capacidad del equipo para impedir la progresión rival en salida de balón.

Fórmula:

```text
Rival salida fallida
──────────────────────────────────────── × 100
Rival salida exitosa + Rival salida fallida
```

---

# 🔶 Construcción

## ✅ Regates

Suma de todos los regates exitosos del equipo.

---

## ❌ Regates

Suma de todos los regates fallidos del equipo.

---

## 📈 Porcentaje de regate

Fórmula:

```text
Regates exitosos
──────────────────────── × 100
Regates exitosos + Regates fallidos
```

---

## ❌ Pérdidas en salida

Suma de todas las pérdidas registradas en salida de balón.

---

## ❌ Pérdidas en construcción

Suma de todas las pérdidas registradas en construcción.

---

# 🎯 Finalización

## 🎯 Tiros fuera

Total de tiros fuera realizados por el equipo.

---

## 🥅 Tiros a puerta

Total de tiros entre los tres palos realizados por el equipo.

---

## ⚽ Goles

Total de goles marcados.

---

## ❌ Pérdidas en finalización

Total de pérdidas registradas durante la fase de finalización.

---

## 🎯 Tiros fuera recibidos

Intentos de finalización del rival fuera de portería.

```text
Evento:
rival_shot_off
```

---

## 🥅 Tiros a puerta recibidos

Intentos de finalización del rival entre los tres palos.

```text
Evento:
rival_shot_target
```

---

## ⚽ Goles recibidos

Goles anotados por el equipo rival.

```text
Evento:
goal_rival
```

---

# 🛡️ Defensa

## 🔁 Recuperaciones en salida

Recuperaciones realizadas durante la salida rival.

---

## 🔁 Recuperaciones en construcción

Recuperaciones realizadas durante la construcción rival.

---

## 🔁 Recuperaciones en finalización

Recuperaciones realizadas durante la finalización rival.

---

## 🔁 Recuperaciones totales

Suma de todas las recuperaciones registradas.

Fórmula:

```text
Recuperaciones salida
+
Recuperaciones construcción
+
Recuperaciones finalización
```

---

# 🟨 Disciplina

## 🤕 Faltas cometidas

Total de faltas realizadas por el equipo.

---

## 🙋 Faltas sufridas

Total de faltas recibidas por el equipo.

---

## 🟨 Amarillas

Total de tarjetas amarillas acumuladas.

---

# 🚀 Estadísticas previstas para Football Scout Analyzer

Las siguientes métricas se generarán posteriormente en Football Scout Analyzer a partir de los JSON exportados:

## Jugadores

- Minutos por temporada
- Valoración media
- Valoración máxima
- Goles
- Recuperaciones
- Pérdidas
- Eficiencia por fase
- Ranking de jugadores

---

## Equipo

- Evolución jornada a jornada
- Rendimiento local / visitante
- Eficacia en salida de balón
- Eficacia de la presión
- Producción ofensiva
- Solidez defensiva
- Comparación entre partidos

---

## Temporada

- Histórico completo
- Clasificaciones internas
- Tendencias
- Dashboard interactivo
- Impacto positivo y negativo de cada jugador
- Informes automáticos## Persistencia

- Guardado automático en Local Storage
- Recuperación automática
- Nuevo partido
- Exportación JSON

---
# 📋 Flujo de trabajo
## Crear partido
Debemos seleccionar:
- Fecha
- Competición
- Equipos (local y visitante)
- Tipo de fútbol (F11 o F8)

## Cargar convocatoria
### Opción A
Podemos importar un fichero en formato TXT con dorsales, nombres, posiciones y TIT o SUP:
``` T;10;Carlos;ED
T;11;Toni;DC

S;12;Jorge;POR
S;13;Adrián;DFC
...
```
### Opción B
Añadir jugadores manualmente.

## Confirmar alineación
- Seleccionamos 11 jugadores u 8 jugadores dependiendo si es F11 o F8
- confirmamos la alineación

## Iniciar partido

Iniciar cronómetro. Y podemos pausar y reiniciar el tiempo.

## Registrar eventos
Para registrar el evento tenemos que:
- Seleccionar jugador.
- Registrar acción.
- Si error, podemos "Deshacer el último evento"
- Aparece un listado con los eventos del partido

## Gestionar cambios
Debemos selccionar el jugador que sale y el que entra.
- Jugador que sale aparecen solamente los que están en el campo actualmente
- Jugador que entra aparecen los que están en el banquillo.
- Un jugador que sale puede volver a entrar

## Finalizar partido
Una vez haya finalizado el partido, debemos:L
- Detener el cronómetro
- Exportar los datos

# ⏱ Control de minutos
La aplicación utiliza un sistema basado en *stints[]* para registrar los periodos de juego.
Por ejemplo:
```
stints: [
    {
        in: 0,
        out: 25
    },
    {
        in: 35,
        out: 60
    }
]
```
Permite:
- Sustituciones ilimitadas
- Reentradas
- Cálculo correcto de minutos jugados

# 💾 Guardado automático

La aplicación guarda automáticamente:
- Convocatoria
- Titulares
- Eventos
- Marcador
- Cronómetro
- Estadísticas
Mediante: *localStorage*
Además, la información se recupera automáticamente al abrir la aplicación.

# 📦 Exportación

El formato es:
```
{
"match": {},
"players": [],
"events": []
}
```

Incluye:
- Datos del partido
- Jugadores
- Cronología completa
- Marcador
- Configuración

# 🎯 Principales resultados obtenidos

La herramienta permite:
- Registro de partidos en tiempo real.
- Seguimiento individual de jugadores.
- Seguimiento colectivo del equipo.
- Cálculo automático de estadísticas.
- Control de minutos jugados.
- Gestión de cambios.
- Exportación de datos.

Todo ello desde un único dispositivo móvil.

# 🏗 Arquitectura

```
index.html

css/
├── style.css
├── layout.css
├── match.css
├── players.css
├── events.css
├── responsive.css

js/
├── state.js
├── app.js
├── timer.js
├── scoreboard.js
├── players.js
├── events.js
├── timeline.js
├── substitutions.js
├── stats.js
├── storage.js
├── export.js
├── ui.js
```

# 🔧 Mantenimiento

## Añadir un nuevo evento
- Modificar: *events.js*
- Añadir: *eventLabel()* y *calculatePlayerStats()*

## Añadir una nueva estadística
- Modificar: *stats.js*
- Actualizar: *renderPlayerStats()* y *renderTeamStats()*

## Añadir nuevos tipos de partido
- Modificar: *state.playersOnField*
- Y en HTML: *<select id="matchType">*

## Copias de seguridad
Exportar periódicamente: *partido.json* para conservar los datos de temporada



