# Proyecto arquitectura de computadoras

Para su instalación siga los siguientes pasos:

### 1. Clonar repositorio

```shell
git clone https://github.com/AdMu2838/Proyecto-Arquitectura-de-computadora.git
```

### 2. Seleccionar mi rama

Las ramas de trabajo disponibles son: feature/Aprendizaje , feature/Test , feature/Juego

```shell
git checkout feature/Nombre_equipo
```
Verificar siempre que se está trabajando en la rama adecuada:

![Ejemplo Rama ](./rama_ejem.png)


### 3. Crear entorno virtual

```shell
python -m venv venv
```

### 4. Activar entorno virtual

```shell
./venv/scripts/activate
```

### 5. Actualizar pip

```shell
python.exe -m pip install --upgrade pip
```

### 6. Instalación de paquetes

```shell
pip install -r requirements.txt
```

### 7. Ejecución del programa

```shell
python project.py
```



#### Nota:

Al usar el comando push desde la rama, hacerlo de la siguiente maner:

```shell
git push origin feature/Nombre_equipo
```

Si no se puede activar el entorno virtual, ejecuta PowerShell como administrador y ejecuta lo siguiente:

```shell
Set-ExecutionPolicy -ExecutionPolicy Bypass
```
