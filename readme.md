# 🔧 Instalación

## Requisitos

- Navegador moderno compatible con JavaScript.
- Safari (iPad recomendado).
- Google Chrome.
- Microsoft Edge.
- Mozilla Firefox.

La aplicación no requiere servidor, base de datos ni instalación de software adicional.

---

## Instalación local

### Opción 1: Descargar el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/USUARIO/datatalk.git
```

o descargar el código fuente en formato ZIP.

Descomprimir el proyecto y abrir:

```text
index.html
```

en cualquier navegador compatible.

---

### Opción 2: GitHub Pages

Acceder directamente a la URL publicada:

```text
https://toni-riso.github.io/datatalk/
```

---

## Instalación como aplicación en iPad

1. Abrir la aplicación en Safari.
2. Pulsar el botón Compartir.
3. Seleccionar:

```text
Añadir a pantalla de inicio
```

4. Confirmar la instalación.

La aplicación aparecerá como una aplicación independiente en el escritorio del iPad.

---

## Primer uso

### 1. Configurar el partido

Introducir:

- Fecha
- Competición
- Campo
- Equipo local
- Equipo rival
- Tipo de partido

```text
F11
F8
```

---

### 2. Cargar la convocatoria

#### Importación desde fichero TXT

Ejemplo:

```text
T;1;Juan;POR
T;2;Pedro;LD

S;15;Héctor;DC
```

Donde:

```text
T = Titular
S = Suplente
```

#### Alta manual

También es posible añadir jugadores manualmente desde el formulario de convocatoria.

---

### 3. Confirmar alineación

Seleccionar los titulares según el tipo de partido:

```text
F11 → 11 jugadores
F8  → 8 jugadores
```

Pulsar:

```text
✅ Confirmar alineación
```

---

### 4. Iniciar partido

Pulsar:

```text
▶ Inicio
```

para iniciar el cronómetro.

---

### 5. Registrar eventos

Seleccionar jugador y registrar la acción correspondiente.

Ejemplo:

```text
D8 Antonio Rivas

✅ Pase bien
✅ Pase bien
🔁 Recuperación
🎯 Tiro
```

---

### 6. Gestionar cambios

Pulsar:

```text
🔄 Cambio
```

Seleccionar:

```text
Sale: 8 Antonio Rivas

Entra: 14 Diego Ruiz
```

y confirmar la sustitución.

---

### 7. Consultar estadísticas

Seleccionando un jugador se muestran:

- Minutos jugados
- Valoración automática
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
- Tarjetas amarillas

---

### 8. Exportar partido

Pulsar:

```text
💾 Exportar Partido
```

Se descargará un fichero JSON con:

- Datos del partido
- Configuración
- Marcador
- Jugadores
- Minutos jugados
- Cambios realizados
- Eventos registrados
- Estadísticas

---

## Guardado automático

La aplicación guarda automáticamente:

- Convocatoria
- Titulares
- Marcador
- Cronómetro
- Eventos
- Cambios
- Estadísticas

mediante:

```text
localStorage
```

La información se recupera automáticamente al volver a abrir la aplicación.

---

## Nuevo partido

Para comenzar un nuevo encuentro:

```text
🆕 Nuevo Partido
```

La aplicación:

- Detiene el cronómetro.
- Elimina los datos almacenados.
- Reinicia completamente el estado del partido.

---

## Actualización del proyecto

Actualizar el repositorio:

```bash
git pull
```

o reemplazar los archivos modificados por la nueva versión.

Si aparecen problemas derivados de la caché del navegador:

```text
Configuración del navegador
→ Eliminar datos del sitio
→ Recargar la aplicación
```
