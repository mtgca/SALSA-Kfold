# GUIA DE EJECUCIÓN DEL EXPERIMENTO

El experimento debe ejecutarse en el servidor A100 utilizando Termius.

## 1. Clonar el repositorio de GitHub

Una vez conectado al servidor A100, navegar al directorio donde se quiera clonar el repositorio. Una vez ahí, utilizar el siguiente comando para clonar el repositorio:

`git clone https://github.com/mtgca/SALSA-Kfold.git`

## 2. Instalar Anaconda

Este experimento utiliza ambientes de Conda. Razón por la cual la instalación de Anaconda es necesaria. Para instalar Anaconda puedes seguir estos pasos:

*	Descargar el instalador de Anaconda desde el sitio oficial. Usar el siguiente comando para descargar la última versión de Anaconda para Linux:

  `wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh`

* Ejecutar el instalador de Anaconda usando el siguiente comando para iniciar la instalación:

  `bash Anaconda3-2023.07-1-Linux-x86_64.sh`

* Seguir las instrucciones de instalación:
   * Acepta el acuerdo de licencia.
   * Especifica el directorio de instalación (por defecto es `~/anaconda3`).
   * Decide si quieres añadir Anaconda al PATH para que esté disponible globalmente en tu sistema. Esto se decide al llegar al siguiente aviso y escribiendo "yes":

  ```bash
  installation finished.
  Do you wish to update your shell profile to automatically initialize conda?
  This will activate conda on startup and change the command prompt when activated.

  If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

  conda config --set auto_activate_base false

  You can undo this by running `conda init --reverse $SHELL`? [yes|no]
  ```



*	Recargar el shell para aplicar los cambios:

  `source ~/.bashrc`
*	Verificar la instalación con el comando:

  `conda --version`

Esto debería completar la instalación de Anaconda en el servidor A100.


## 3. Creación de ambiente.

Una vez ejecutados los pasos 1 y 2, la terminal dentro del servidor A100 en Termius debería verse de la siguiente manera:

  ```
  (base) username@deeplearning-srv:~$ conda --version
  conda 23.5.2
  (base) username@deeplearning-srv:~$ ls
  anaconda3  Anaconda3-2023.07-1-Linux-x86_64.sh  SALSA-Kfold
  ```

Para continuar con el desarrollo del experimento es necesario:

* Navegar al directorio del repositorio:

  `cd SALSA-Kfold`

* Crear un ambiente Conda con el archivo py37.yml:

  `conda env create -f py37.yml`

* Activar el ambiente con:

  `conda activate py37`


## 2. Obtener la base de datos
Para este experimento se utilizó la base de datos TAU-NIGENS Spatial Sound Events 2021, que se puede obtener en el siguiente link: https://zenodo.org/records/4844825

No es necesario descargar el formato MIC, únicamente hacerlo con FOA, ya que es el formato en el que se trabajó esta experimentación. Una vez descargado el dataset, organizarlo según la estructura planteada en el repositorio original https://github.com/thomeou/SALSA :
```
./
├── feature_extraction.py
├── ...
└── data/
    ├──foa_dev
    │   ├── fold1_room1_mix001.wav
    │   ├── fold1_room1_mix002.wav  
    │   └── ...
    ├──foa_eval
    ├──metadata_dev
    ├──metadata_eval (might not be available yet)
    ├──mic_dev
    └──mic_eval
  ```

Se detallan las snstrucciones paso a paso para descargar, instalar zip, y descomprimir los archivos `foa_dev` y `metadata_dev`:
* Crear la carpeta data en el directorio `SALSA-Kfold`

  Primero, navega al directorio SALSA-Kfold y crea una carpeta llamada data para almacenar los archivos descargados:
```
cd ~/SALSA-Kfold
mkdir data
```


* Mover el archivo `metadata_eval` ya existente en el repositorio dentro de la carpeta `data`

  Una vez clonado el repositorio, ubicarse en el directorio del mismo:

  `cd ~/SALSA-Kfold`

  Se encuentra dentro de este directorio el archivo `metadata_eval.zip`. Moverlo dentro del directorio `data` recientemente creado:

  `mv metadata_eval.zip data`
  
  Este paso asegura que todos los archivos se almacenarán en la carpeta `data` dentro del directorio `SALSA-Kfold`.

* Descargar el archivo `foa_dev.z01`

  Usar `wget` para descargar el archivo `foa_dev.z01` desde el enlace de Zenodo:

  `wget https://zenodo.org/record/4844825/files/foa_dev.z01?download=1 -O foa_dev.z01`

* Descargar el archivo `foa_dev.zip`

  De manera similar, descarga el archivo principal `foa_dev.zip`:

  `wget https://zenodo.org/record/4844825/files/foa_dev.zip?download=1 -O foa_dev.zip`

* Descargar el archivo `foa_eval.zip`

  De manera similar, descarga el archivo principal `foa_dev.zip`:

  `wget https://zenodo.org/record/4844825/files/foa_dev.zip?download=1 -O foa_eval.zip`

* Descargar el archivo `metadata_dev.zip`

  Por último, descarga el archivo `metadata_dev.zip` que contiene los metadatos necesarios para el experimento:

  `wget https://zenodo.org/record/4844825/files/metadata_dev.zip?download=1 -O metadata_dev.zip`

* Instalar zip (en caso de que no esté instalado)

  Cuando se intente combinar los archivos utilizando el comando zip, puede que el sistema indique que zip no está instalado. Si recibe un error como este, seguir estos comandos:
```
sudo apt update
sudo apt install zip
```
Nota: Si no tiene permisos sudo o acceso a la cuenta root, puesto que el sistema le solicitará que ingrese su clave de usuario respectiva, necesitará contactar al administrador del sistema para que lo haga en su lugar.

* Combinar las partes del archivo `foa_dev`

  Después de instalar zip, puedes combinar las partes del archivo:

  `zip -s 0 foa_dev.zip --out sfoa_dev.zip`

  Este comando combinará las dos partes en un solo archivo llamado `sfoa_dev.zip`.

* Descomprimir el archivo combinado

  Una vez que hayas combinado los archivos, puedes descomprimir el archivo `sfoa_dev.zip` utilizando el comando unzip:

  `unzip sfoa_dev.zip`

  Este comando extraerá los archivos en el directorio actual.

* Descomprimir el archivo `foa_eval.zip`

  Descomprimir el archivo `sfoa_dev.zip` utilizando el comando unzip:

  `unzip sfoa_dev.zip`

  Este comando extraerá los archivos en el directorio actual.

* Descomprimir el archivo `metadata_dev.zip`

  Descomprimir el archivo `metadata_dev.zip` con el siguiente comando:

  `unzip metadata_dev.zip`

  Esto extraerá los metadatos necesarios para el proyecto en el directorio actual.

* Descomprimir el archivo `metadata_eval.zip`

  Finalmente, Descomprimir el archivo `metadata_eval.zip` con el siguiente comando:

  `unzip metadata_eval.zip`

* Verificar el contenido

  Para verificar que todos los archivos se hayan descargado y descomprimido correctamente, se puede listar el contenido del directorio data:

  `ls`

  Se deben ver las carpetas y archivos descomprimidos correspondientes a `foa_dev`, `foa_eval`, `metadata_eval` y `metadata_dev`:

  ```
  (base) username@deeplearning-srv:~/SALSA-Kfold/data$ ls
foa_dev  foa_dev.z01  foa_dev.zip  foa_eval  foa_eval.zip  metadata_dev  metadata_dev.zip  metadata_eval metadata_eval.zip sfoa_dev.zip
  ```

### Resumen de comandos

Crear la carpeta data:

* `cd ~/SALSA-Kfold`

* `mkdir data`

* `mv metadata_eval.zip data

* `cd data`

Descargar los archivos:

* `wget https://zenodo.org/record/4844825/files/foa_dev.z01?download=1 -O foa_dev.z01`

* `wget https://zenodo.org/record/4844825/files/foa_dev.zip?download=1 -O foa_dev.zip`

* `wget https://zenodo.org/record/4844825/files/foa_dev.zip?download=1 -O foa_eval.zip`

* `wget https://zenodo.org/record/4844825/files/metadata_dev.zip?download=1 -O metadata_dev.zip`

Instalar zip (en caso necesario):

* `sudo apt update`

* `sudo apt install zip`

Combinar y descomprimir los archivos:

* `zip -s 0 foa_dev.zip --out sfoa_dev.zip`

* `unzip sfoa_dev.zip`

* `unzip foa_eval.zip`

* `unzip metadata_dev.zip`

* `unzip metadata_eval.zip`

## 3. Configuración de experimento
- Ejecutar el script `make_folds.py`
- Antes de entrenar el modelo se deben extraer las features de acuerdo a necesidad:
  -   Para extraer SALSA se debe editar el archivo `tnsse_2021_salsa_feature_config.yml` que está en la ruta `dataset\configs\`. `data_dir` hace referencia a donde está la base de datos, y `feature_dir` es dónde queremos que se guarden las features extraídas. Una vez configurado, con el ambiente de conda activo, ejecutar el siguiente comando `make salsa`.
  -   Para linspeciv y melspeciv el proceso es igual, la ruta de archivo es la misma, pero ahora se debe configurar `tnsse_2021_salsa_lite_feature_config.yml`. Luego de eso, ejecutar el comando `make feature`
- La extracción de características toma su tiempo...
- Una vez extraídas todas las características que se deseen, se debe ir al archivo de configuración `seld.yml` en la ruta `experiments\configs\` y lo único que se debe cambiar es:
  -  `feature_root_dir` (ruta de las features extraídas)
  -  `gt_meta_root_dir` (ruta de la metadata)
  -  `feature_type` (qué tipo de features usar para train)
  -  `mode: 'crossval'`
  -  `audio_format: 'foa'`
  -  `train_batch_size: 32`  # Reduce batch size if GPU is out of memory
  -  `max_epochs: 50` # epoch counting from [0 to n-1]
  
## 4. Cambios en el código de acuerdo a la DAT requerida
Un el archivo `dataset/datamodule.py` existe la clase SeldDataModule la cual contiene las configuraciones de data augmentation on the fly. Los cambios se deben hacer en el formato FOA entonces cualquier cambio solo se realiza de la línea 45 a la 71.
- Primero, setear esta variable `self.train_joint_transform = None`
- La variable `self.train_transform = ComposeTransformNp([])` debe tener los valores de la(s) DAT(s) que vayamos a usar:
  - RANDOM CUTOUT: RandomCutoutNp(always_apply=True, image_aspect_ratio=self.feature_db.train_chunk_len / 200, n_zero_channels=3)
  - CHANNEL SWAPPING: TfmapRandomSwapChannelFoa(n_classes=feature_db.n_classes)
  - FREQUENCY SHIFT: RandomShiftUpDownNp(freq_shift_range=10)
  - Por ejemplo si se desea realizar RC + CS la variable debe ser:
```
self.train_transform = ComposeTransformNp([
                          RandomCutoutNp(always_apply=True, image_aspect_ratio=self.feature_db.train_chunk_len / 200, n_zero_channels=3),
                          TfmapRandomSwapChannelFoa(n_classes=feature_db.n_classes)])
```
- En caso de no querer DAT simplemente setear en `None`
## 5. Ejecutar el experimento
Una vez todo ha sido configurado de acuerdo a la necesidad, se debe ubicar en el directorio general del proyecto y ejecutar el comando `nohup make train &` (asegurarse de tener instalado nohup). Este comando comenzará a entrenar el modelo en segundo plano, para revisar el estado (épocas, métricas, etc.) se debe ejecutar el comando `cat nohup.out`.\
Los resultados se irán guardando en una carpeta llamada `\Outputs`.

En caso de que el proceso termine inesperadamente (sea por un apagón de luz, colapso del servidor, etc.) ir al archivo `Makefile` y cambiar la configuración a `RESUME=True` línea 33 del archivo. Una vez realizado el cambio, ejecutar nuevamente el comando `nohup make train &`, esto reanudará el entrenamiento.

**Nota:** La lógica de reanudación busca el último fold que se estaba ejecutando antes de la interrupción y vuelve a entrenar desde la época 0 de dicho fold. Por lo tanto, se debe borrar los resultados de las épocas que ya se habían ejecutado de dicho fold en las carpetas checkpoint, best para evitar duplicados y confusión.
