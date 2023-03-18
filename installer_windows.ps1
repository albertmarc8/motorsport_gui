if (!(Get-Command python.exe -ErrorAction SilentlyContinue)) {
    # si no se encuentra el archivo "python.exe", se ejecuta este bloque de código
    # Descargar archivo de instalación de Python
    $descarga = Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" -OutFile "$env:TEMP\python-3.10.0-amd64.exe"

    # Instalar Python
    Start-Process "$env:TEMP\python-3.10.0-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

# Instalar dependencias de Python usando pip
pip install matplotlib pandas customtkinter

# Crear acceso directo al archivo .py
# con Start-Process se puede ocultar la terminal
$sh = New-Object -ComObject WScript.Shell
$nombre_acceso_directo = "UJI Motorsport Plotter"
$ruta_archivo_py = ($PWD.path, "\main.py") -join ""
$ruta_acceso_directo = $sh.SpecialFolders("Desktop") + "\" + $nombre_acceso_directo + ".lnk"
$archivo_objetivo = $sh.CreateShortcut($ruta_acceso_directo)
$archivo_objetivo.TargetPath = "python.exe"
$archivo_objetivo.Arguments = "`"$ruta_archivo_py`""
$archivo_objetivo.WorkingDirectory = $PWD.path
$archivo_objetivo.Save()
