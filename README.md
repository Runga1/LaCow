# LaCow

Proyecto de analítica ganadera para simular escenarios de compra, engorde y venta de ganado, evaluando utilidad, ROI, precio de equilibrio y sensibilidad ante cambios en precio, costos y peso.

## Estructura del proyecto

- `data/raw/`: archivos de entrada, como `escenarios_ganado.xlsx`
- `outputs/`: archivos de salida, como resultados, sensibilidad y top escenarios
- `src/models/`: lógica de simulación, análisis, sensibilidad y gráficos
- `src/data/`: lectura de archivos de entrada
- `src/utils/`: funciones auxiliares

## Módulos implementados

- `simulador_ganado.py`: calcula rentabilidad de un escenario
- `simulador_escenarios.py`: genera combinaciones de escenarios
- `procesar_escenarios_excel.py`: lee escenarios desde Excel y produce resultados
- `analizar_resultados.py`: identifica escenarios viables y rankings
- `sensibilidad.py`: evalúa cambios en precio, costo y peso
- `graficar_sensibilidad.py`: genera gráficos de sensibilidad

## Cómo ejecutar

### 1. Procesar escenarios desde Excel
```bash
python -m src.models.procesar_escenarios_excel