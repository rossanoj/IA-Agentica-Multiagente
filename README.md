# IA-Agentica-Multiagente
Proyecto Final IBM Ingenieria IA - Modelo IA Agentica Multiagente. (Coursera) 

## Configuracion del proyecto

### Usuario Git asociado al proyecto

Para definir la identidad de Git solamente para este repositorio, ejecuta estos comandos desde su carpeta:

```bash
git config --local user.name "Tu nombre"
git config --local user.email "tu-correo@example.com"
```

Comprueba la configuracion con:

```bash
git config --local --list
```

Estos valores se guardan en `.git/config` y no modifican la configuracion global de Git del equipo.

### Token de Hugging Face

Crea el token desde la configuracion de acceso de Hugging Face con estas opciones:

- Tipo de token: `Fine-grained`.
- Permiso: habilitar el acceso de inferencia (`Inference` o `Make calls to Inference Providers`, segun la interfaz).

Usa el token generado en los siguientes comandos como `HF_TOKEN`.

### Token en Linux

Define el token como variable de entorno para la sesion actual:

```bash
export HF_TOKEN="tu-token"
```

Para dejarlo disponible en nuevas sesiones de Bash, agrega la misma linea a `~/.bashrc` y recarga la configuracion:

```bash
source ~/.bashrc
```

### Token en Windows

En PowerShell, para la sesion actual:

```powershell
$env:HF_TOKEN = "tu-token"
```

Para guardarlo en las nuevas sesiones del usuario de Windows:

```powershell
[Environment]::SetEnvironmentVariable("HF_TOKEN", "tu-token", "User")
```

En `cmd.exe`, usa `set` para la sesion actual o `setx` para las nuevas sesiones:

```bat
set HF_TOKEN=tu-token
setx HF_TOKEN "tu-token"
```

Verifica que la variable este definida sin mostrar el token completo:

```bash
echo "${HF_TOKEN:0:4}..."
```

En PowerShell:

```powershell
$env:HF_TOKEN.Substring(0, 4) + "..."
```

No incluyas el token en el codigo, en archivos versionados ni en la URL del remoto.

### Base vectorial local con ChromaDB

La base vectorial local para el sistema RAG se guarda en la carpeta `localdb`.
Esta carpeta esta excluida de Git porque contiene datos generados localmente y
debe crearse de nuevo en cada entorno.

Instala las dependencias del proyecto:

```powershell
pip install -r requirements.txt
```

Ejecuta esta celda de Python o de un notebook para crear la base y la
coleccion que usara el sistema RAG:

```python
from pathlib import Path

import chromadb

db_path = Path("localdb")
db_path.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(db_path))
collection = client.get_or_create_collection(name="documentos")
```

Despues de crear la coleccion, agrega los documentos y sus embeddings siguiendo
el flujo de ingesta del notebook. No subas la carpeta `localdb` al repositorio.
