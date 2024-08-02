# GUIA DE EJECUCIÓN DEL EXPERIMENTO
## 1. Creación de ambiente.
Asegurarse de tener conda instalado en su computador. Con el archivo salsa_environment.yml se debe crear un ambiente con todas las librerías requeridas para el experimento\
Usar el comando `conda env create -f py37.yml`
## 2. Obtener la base de datos
Para este experimento se utilizó la base de datos TAU-NIGENS Spatial Sound Events 2021, que se puede obtener en el siguiente link: https://zenodo.org/records/4844825\
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
  -  `max_epochs: 50` # epoch counting from [0 to n-1],
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
