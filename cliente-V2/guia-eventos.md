# ⚡ Tabla rápida de decisión

Esta tabla permite decidir rápidamente qué evento registrar durante el partido.

Ante una acción dudosa, busca primero la fase del juego y después el resultado de la acción.

---

## ⚽ Salida de balón

| Situación | Evento |
|------------|---------|
| El equipo consigue superar la presión rival y progresar | ✅ Salida exitosa |
| El equipo pierde el balón o no consigue progresar | ❌ Salida fallida |
| Un jugador pierde el balón durante la salida | ❌ Pérdida salida |
| El rival supera nuestra presión | ✅ Rival salida exitosa |
| Nuestra presión provoca pérdida o despeje rival | ❌ Rival salida fallida |

---

## 🔶 Construcción

| Situación | Evento |
|------------|---------|
| Jugador supera a un rival manteniendo la posesión | ✅ Regate |
| Jugador intenta superar a un rival y pierde la posesión | ❌ Regate |
| Jugador pierde el balón durante la elaboración | ❌ Pérdida construcción |

---

## 🎯 Finalización

| Situación | Evento |
|------------|---------|
| Disparo fuera de portería | 🎯 Tiro fuera |
| Disparo entre los tres palos | 🥅 Tiro a puerta |
| Gol anotado | ⚽ Gol |
| Pérdida de balón en zona de finalización | ❌ Pérdida finalización |
| Tiro rival fuera | 🎯 Rival tiro fuera |
| Tiro rival a portería | 🥅 Rival tiro a puerta |
| Gol rival | ⚽ Gol rival |

---

## 🛡️ Defensa

| Situación | Evento |
|------------|---------|
| Recuperación durante la salida rival | 🔁 Recuperación salida |
| Recuperación durante la construcción rival | 🔁 Recuperación construcción |
| Recuperación cerca de nuestra portería | 🔁 Recuperación finalización |

---

## 🟨 Disciplina

| Situación | Evento |
|------------|---------|
| El jugador hace falta | 🤕 Falta cometida |
| El jugador recibe falta | 🙋 Falta sufrida |
| El jugador recibe amarilla | 🟨 Amarilla |

---

# 🤔 Casos especiales y situaciones dudosas

---

## El defensa da un pelotazo largo para evitar riesgos

### ¿Salida exitosa o fallida?

**Salida exitosa** únicamente si el equipo mantiene la posesión y supera la presión.

```text
Portero
↓
Central
↓
Pelotazo
↓
Nuestro delantero controla

✅ Salida exitosa
```

---

### Si se pierde la posesión

```text
Portero
↓
Central
↓
Pelotazo
↓
Recupera rival

❌ Salida fallida
```

---

## Un jugador recibe, controla mal y pierde el balón

### ¿Pérdida salida o pérdida construcción?

Depende de dónde ocurre.

```text
Cerca de la propia área
```

↓

```text
❌ Pérdida salida
```

---

```text
En zona media
```

↓

```text
❌ Pérdida construcción
```

---

## Un jugador intenta un regate y pierde el balón

Registrar:

```text
❌ Regate
```

No añadir además:

```text
❌ Pérdida construcción
```

porque ya queda contabilizada en el regate fallido.

---

## Un delantero dispara y marca

Registrar únicamente:

```text
⚽ Gol
```

No registrar además:

```text
🥅 Tiro a puerta
```

ni

```text
🎯 Tiro fuera
```

El gol ya representa la acción final.

---

## El portero rival para un disparo

Registrar:

```text
🥅 Tiro a puerta
```

porque el balón iba entre los tres palos.

---

## Tiro al palo

Criterio recomendado:

```text
🥅 Tiro a puerta
```

porque la trayectoria iba dirigida a portería.

Mantener siempre el mismo criterio durante toda la temporada.

---

## Centro al área que nadie remata

No registrar nada.

No es una finalización.

---

## Recuperación tras una mala entrega rival en campo propio

Si se produce durante la presión a la salida rival:

```text
🔁 Recuperación salida
```

---

## Recuperación en mediocampo

```text
🔁 Recuperación construcción
```

---

## Recuperación dentro o cerca del área propia

```text
🔁 Recuperación finalización
```

---

## El rival pierde el balón solo

Aunque el error sea suyo, si recuperamos la posesión debemos registrar recuperación:

```text
🔁 Recuperación salida
```

o

```text
🔁 Recuperación construcción
```

o

```text
🔁 Recuperación finalización
```

según la situación.

---

## Falta y amarilla

Registrar dos eventos:

```text
🤕 Falta cometida

🟨 Amarilla
```

---

## Falta recibida y posterior amarilla del rival

Registrar únicamente:

```text
🙋 Falta sufrida
```

No registramos tarjetas rivales.

---

# 📏 Regla de oro

Ante cualquier duda:

### ¿Tenemos balón?

```text
Salida
Construcción
Finalización
```

---

### ¿No tenemos balón y lo recuperamos?

```text
Recuperación
```

---

### ¿Hay infracción?

```text
Disciplina
```

---

### ¿Genera ocasión?

```text
Finalización
```

---

# 🎯 Objetivo principal

La prioridad no es registrar cada detalle del partido.

La prioridad es que:

```text
La misma acción
↓
Se registre siempre igual
↓
Durante toda la temporada
```

Esto garantiza estadísticas fiables y análisis consistentes posteriores en Football Scout Analyzer.
