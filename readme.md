# POC ETL en Google Cloud Platform

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) utilizando servicios de Google Cloud Platform. El pipeline procesa archivos CSV y Excel, validando su contenido y almacenándolo en una base de datos PostgreSQL.

## Arquitectura

```
Fuente externa  →  Cloud Storage (5 GB gratis/mes)
                     │
 Cloud Run (2 M invocaciones gratis/mes)
   (transforma & valida)
                     │
     Compute Engine e2-micro  (PostgreSQL 16)
                     │
   Cloud Logging / Monitoring
                     │
         Pub/Sub (mensajes de estado)
```

## Componentes Principales

1. **Servicio de Procesamiento (Cloud Run)**
   - Implementado en Python con Flask
   - Procesa archivos CSV y Excel
   - Realiza validaciones de calidad de datos
   - Notifica el estado del proceso vía Pub/Sub

2. **Base de Datos (PostgreSQL)**
   - Alojada en una instancia e2-micro de Compute Engine
   - Acceso privado mediante VPC Connector
   - Almacena los datos procesados

3. **Mensajería (Pub/Sub)**
   - Topics para éxitos y errores
   - Monitoreo del estado del pipeline

## Requisitos

- Python 3.12
- Dependencias listadas en `requirements.txt`
- Cuenta de Google Cloud Platform
- Servicios GCP habilitados (ver `1uno.bash`)

## Configuración

El proyecto incluye scripts bash numerados para la configuración paso a paso:

1. `1uno.bash`: Configuración inicial del proyecto y servicios GCP
2. `2dos.bash`: Creación de instancia para PostgreSQL
3. `3tres.bash`: Instalación y configuración de PostgreSQL
4. `4cuatro.bash`: Configuración de red privada
5. `5cinco.bash`: Creación de topics Pub/Sub
6. `6seis.bash`: Configuración de Artifact Registry
7. `7siete.bash`: Despliegue en Cloud Run
8. `8ocho.bash`: Monitoreo de logs
9. `9nueve.bash`: Pruebas con archivos demo

## Estructura del Proyecto

- `main.py`: Servicio principal (Flask)
- `Dockerfile`: Configuración de contenedor
- `requirements.txt`: Dependencias Python
- `demo1.csv` y `demo1.txt`: Archivos de prueba
- Scripts bash numerados del 1 al 9 para despliegue

## Variables de Entorno

El servicio requiere las siguientes variables de entorno:
- `PG_HOST`: Host de PostgreSQL
- `PG_DB`: Nombre de la base de datos
- `PG_USER`: Usuario de PostgreSQL
- `PG_PWD`: Contraseña de PostgreSQL

## Despliegue

1. Ejecutar los scripts bash en orden numérico
2. Construir y subir la imagen Docker:
   ```bash
   gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/poc/pipeline:0.1
   ```
3. Desplegar en Cloud Run:
   ```bash
   gcloud run deploy pipeline [opciones]
   ```

## Monitoreo

- Logs de Cloud Run disponibles vía `8ocho.bash`
- Mensajes de estado en topics Pub/Sub
- Métricas disponibles en Cloud Monitoring

## Seguridad

- Acceso a PostgreSQL solo mediante VPC Connector
- Credenciales gestionadas mediante variables de entorno
- Service Account dedicado para Cloud Run

## Limitaciones

- Procesa archivos CSV y Excel únicamente
- Validaciones básicas de calidad de datos
- Diseñado para cargas de trabajo moderadas

## Licencia

Este proyecto está bajo la licencia MIT.

         