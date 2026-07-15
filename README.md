# Virus Shimeji

Este proyecto es un shimeji hecho en Python con PyQt6. El personaje aparece en pantalla, reacciona al cursor y cambia de animación según lo que pasa (quieto, caminando, durmiendo, huyendo, etc.).

> Recomendación importante: este proyecto está pensado para Windows 10/11/8.5/7. Por eso el empaquetado se recomiendan hacer en ese sistema operativo.

## Requisitos

Antes de empezar, asegúrate de tener instalado:

- Python 3.10 o superior (recomendado 3.10 o 3.11)
- Git (opcional, si vas a clonar el repositorio)
- Windows 10 o 11 (recomendado para probar y empaquetar)

## 1) Descargar o clonar el proyecto

Si lo tienes como ZIP:

1. Descarga el repositorio.
2. Descomprime la carpeta.
3. Entra a la carpeta del proyecto.

Si lo vas a clonar con Git:

```powershell
git clone https://github.com/VICTORONJA-MN/virus_shimeji.git
cd virus_shimeji
```

## 2) Crear un entorno virtual en modo dev y para empaquetar (muy recomendable)

para evitar conflictos con otros paquetes de Python que tengas instalados.

En PowerShell, ejecuta:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Si PowerShell te bloquea la activación del entorno virtual, ejecuta esto antes:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## 3) Instalar las dependencias

Desde la carpeta del proyecto:

```powershell
pip install -r requisitos.txt
```

Eso instalará:

- PyQt6
- PyInstaller

## 4) Ejecutar en modo desarrollo

Este modo sirve para probar el proyecto directamente desde el código fuente.

```powershell
python main.py
```

También puedes abrir la carpeta en VS Code y ejecutar el archivo main.py desde el botón de Run o con F5.

### en "modo desarrollo"

- se ejecuta el código fuente directamente.
- Se recomienda hacerlo en Windows, porque el proyecto usa funciones específicas de ese sistema.

## 5) Ejecución en fase de producción

En el modo normal se ejecuta el archivo .exe generado por PyInstaller.

Primero debes empaquetar la app (ver siguiente sección). Luego podrás ejecutar el .exe generado en:

nota: Como el archivo está pensado para simular un "virus" no existe un boton para cerrar el programa por lo que para matar el proceso se debe hacer desde la terminal o desde el adminstrador de tareas. Se encuentra como "Cafe.exe".

```powershell
dist\main\main.exe
```

## 6) Empaquetar la app como .exe

Este proyecto ya incluye el archivo de configuración de PyInstaller: main.spec.

Para generar el ejecutable, ejecuta:

```powershell
pyinstaller main.spec
```

El resultado quedará en:

```powershell
dist\main\main.exe
```

### Si quieres limpiar los builds anteriores

```powershell
Remove-Item -Recurse -Force build, dist
pyinstaller main.spec
```

## 8) Problemas que puden surgir

### Error: `No module named PyQt6`

Significa que las dependencias no están instaladas o no estás en el entorno virtual correcto.

Haz esto:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requisitos.txt
```

### Error al activar el entorno virtual

Si PowerShell no deja activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### El ejecutable no encuentra los archivos de `assets`

Asegúrate de haber ejecutado:

```powershell
pyinstaller main.spec
```

El archivo main.spec ya está preparado para incluir la carpeta assets.

## Resumen rápido

### Desarrollo

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requisitos.txt
python main.py
```

### Empaquetar a .exe

```powershell
pip install -r requisitos.txt
pyinstaller main.spec
```

## Resultado esperado

- Una app ejecutable en modo normal (`.exe`).
- Un entorno de desarrollo listo para modificar el proyecto.
- Una versión lista para probar en Windows con los gifs incluidos en la carpeta assets.
