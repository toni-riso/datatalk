# ⚽ DataTalk

Aplicación web progresiva (PWA) para el registro y análisis de eventos de fútbol en tiempo real.

Diseñada para ser utilizada principalmente desde iPad durante partidos de Fútbol 11 o Fútbol 8.

[¡Ver demo cliente!](https://toni-riso.github.io/datatalk/cliente/)

[Plantilla ejemplo F11](plantilla-F11.txt)

[Plantilla ejemplo F8](plantilla-F8.txt)

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

## Eventos registrados

### Construcción

- Pase correcto
- Pase incorrecto

### Regate

- Regate correcto
- Regate incorrecto

### Finalización

- Tiro
- Tiro a puerta
- Gol

### Defensivos

- Recuperación
- Pérdida

### Disciplina

- Falta cometida
- Falta recibida
- Tarjeta amarilla

### Partido

- Cambio de jugador
- Gol rival

## Cronología

- Registro automático de eventos
- Línea temporal del partido
- Deshacer último evento

## Estadísticas

### Jugador

- Pases correctos
- Pases incorrectos
- Porcentaje de pase
- Regates correctos
- Regates incorrectos
- Porcentaje de regate
- Tiros
- Tiros a puerta
- Goles
- Recuperaciones
- Pérdidas
- Faltas cometidas
- Faltas sufridas
- Amarillas
- Minutos jugados
- Valoración automática

### Equipo

- Estadísticas agregadas
- Porcentajes globales
- Producción ofensiva
- Producción defensiva

## Persistencia

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



