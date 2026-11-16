# Laboratorio-11-DASHBOARD


Dashboard en Streamlit elaborado por Sebastian Rojas y Juan Diego Moreno para conocer a los clientes de KORA y responder el laboratorio 11.

🔗 **App publicada:** https://laboratorio-11-dashboard-acd.streamlit.app

## Qué muestra
- KPIs: compradores, pedidos, ingreso, tasa de recompra, clientes con exactamente una compra y su porcentaje.
- Clientes por segmento e ingreso por preferencia declarada.
- Tasa de recompra por canal (con el número de compradores detrás de cada tasa).
- Clientes con un solo pedido por canal.
- Filtros por ciudad, canal, segmento y preferencia declarada.
- Recomendación de canal para un piloto de segunda compra.

## Archivos
| Archivo | Contenido |
|---|---|
| `LAB11.py` | Código del dashboard |
| `KORA_clientes.csv` | 1 fila = 1 cliente registrado |
| `KORA_pedidos.csv` | 1 fila = 1 pedido |
| `requirements.txt` | Librerías necesarias |

## Cómo ejecutarlo localmente
```bash
pip install -r requirements.txt
streamlit run LAB11.py
```

*Curso DATA1002 – Aplicaciones en Ciencia de Datos, Universidad de los Andes. Datos con fecha de corte 31/10/2026.*
