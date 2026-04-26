# Optimización Lab: Hill Climbing & Simulated Annealing

Bienvenido al laboratorio visual de algoritmos de optimización. Este proyecto permite visualizar en tiempo real cómo funcionan las búsquedas locales y comparar su eficiencia.

## Equipo de Trabajo
* **Aldo** (Líder de Proyecto & Arquitectura Base)
* **Integrante 1** (Módulo: Hill Climbing)
* **Integrante 2** (Módulo: Simulated Annealing)
* **Integrante 3** (Módulo: Comparativa de Resultados)

---

## Guía de Inicio Rápido (Local)

Sigue estos pasos para tener el proyecto corriendo en tu computadora en menos de 2 minutos:

### 1. Requisitos Previos
Asegúrate de tener instalado **Node.js** (Versión 18 o superior). Puedes descargarlo en [nodejs.org](https://nodejs.org/).

### 2. Instalación
Clona el repositorio o descarga la carpeta, abre una terminal en la raíz del proyecto y ejecuta:

```bash
# Entrar a la carpeta del proyecto
cd proyecto-algoritmos

# Instalar todas las dependencias necesarias
npm install
```

### 3. Ejecución
Para lanzar el servidor de desarrollo:

```bash
npm run dev
```
Una vez ejecutado, abre tu navegador en: [http://localhost:5173](http://localhost:5173)

---

## Estructura del Proyecto (Dónde trabajar)

Cada uno tiene una carpeta asignada para evitar conflictos en Git. **No toques archivos fuera de tu carpeta** a menos que sea necesario:

* **Hill Climbing:** `src/components/HillClimbing/`
* **Simulated Annealing:** `src/components/SimulatedAnnealing/`
* **Comparativa:** `src/components/Comparison/`

Los estilos globales y el enrutado principal están en `src/App.jsx`.

---

## Herramientas Incluidas
* **Vite + React:** Para una carga ultra rápida.
* **Lucide React:** Biblioteca de iconos (usa `import { IconName } from 'lucide-react'`).
* **CSS-in-JS:** Estilos modulares para mantener la interfaz limpia.
