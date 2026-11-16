#codigo de clase
import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px 

df_clientes= pd.read_csv("data/KORA_clientes.csv", parse_dates=["fecha_registro"])
df_pedidos=pd.read_csv("data/KORA_pedidos.csv", parse_dates=["fecha_pedido"])

st.title("KORA - Clientes")
st.caption("Elaborado con datos de clientes")
st.sidebar.header("FILTROS")
filtro_canal=st.sidebar.multiselect(label="CANALES",
                                    options=df_clientes.canal_adquisicion.unique(),
                                    default=df_clientes.canal_adquisicion.unique())

filtro_ciudad=st.sidebar.multiselect(label="CIUDAD",
                                    options=df_clientes.ciudad.unique(),
                                    default=df_clientes.ciudad.unique())

filtro_segmento=st.sidebar.multiselect(label="SEGMENTO",
                                       options=["Sin Compra", "Primerizo", "En Desarrollo", "Fiel", "En Pausa"],
                                       default=["Sin Compra", "Primerizo", "En Desarrollo", "Fiel", "En Pausa"])  

df_intermedio=(df_pedidos.groupby("id_cliente", as_index=False)
               .agg(n_pedidos=("id_pedido", "count"),
                    ingreso_total=("ingreso_neto_cop", "sum"),
                    fecha_ultimo_pedido=("fecha_pedido", "max"))
               )

df_intermedio["n_pedidos"]=df_intermedio["n_pedidos"].fillna("Sin Compra")
df_intermedio["resencia"]=(pd.Timestamp.today() - df_intermedio["fecha_ultimo_pedido"]).dt.days  

def asignar_segmento(n_pedidos, tiempo):
    segmento = ""
    if n_pedidos==0:
        segmento = "Sin Compra"
    elif n_pedidos== 1 and tiempo <= 90:
        segmento = "Primerizo"
    elif n_pedidos==2 and tiempo<= 90:
        segmento = "En Desarrollo"
    elif n_pedidos>=3 and tiempo<= 90:
        segmento = "Fiel"
    elif n_pedidos >= 1 and tiempo > 90:
        segmento = "En Pausa"  
    return segmento 

df_intermedio["segmento"]=(df_intermedio
                           .apply(lambda x: asignar_segmento(x["n_pedidos"], x["resencia"]), axis=1)
                           )    
df_clientes_filtrado=df_clientes[(df_clientes.canal_adquisicion.isin(filtro_canal)) & (df_clientes.ciudad.isin(filtro_ciudad))]  
df_final=df_clientes_filtrado.merge(df_intermedio, how="left", on="id_cliente")
df_final["segmento"]=df_final["segmento"].fillna("Sin Compra")  
df_final=df_final[df_final.segmento.isin(filtro_segmento)]

compradores=df_final.query("n_pedidos>0").shape[0]
pedidos=df_final.n_pedidos.sum()
ingreso=df_final.ingreso_total.sum()
recompra=f"{(df_final.query('n_pedidos>1').shape[0])/df_final.shape[0]*100 :.2f}%"  

a, b, c, d=st.columns(4)
a.metric(label="COMPRADORES", value=compradores, border=True)
b.metric(label="PEDIDOS", value=pedidos, border=True)
c.metric(label="INGRESO", value=ingreso, border=True)
d.metric(label="RECOMPRA", value=recompra, border=True)

st.divider()

derecha, izquierda = st.columns(2)

with derecha:
    df_plot=(df_final.groupby("segmento", as_index=False)
             .agg(n_clientes=("id_cliente", "count")))
    fig=px.bar(data_frame=df_plot, x="segmento", y="n_clientes", color="segmento", text="n_clientes")
    fig.update_layout(xaxis_title="Segmento", yaxis_title="Número de Clientes", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
with izquierda:
    df_plot=(df_final.groupby("preferencia_declarada", as_index=False)
             .agg(ingreso=("ingreso_total", "sum")).sort_values(by="ingreso", ascending=False))  
    fig=px.bar(data_frame=df_plot, x="ingreso", y="preferencia_declarada", orientation="h")
    fig.update_layout(xaxis_title="Ingreso", yaxis_title="Departamento", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)