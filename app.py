# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 19:13:05 2025

@author: ciencia.dados1
"""
from dash .dependencies import Output, Input
import pandas as pd 
import sqlite3
import plotly.express as px 
import dash 
import dash_bootstrap_components as dbc 
from dash import dcc, html  # ✅ Importação adicionada para usar html.H1

conexao = sqlite3.connect("db/loja1.db")

script = "SELECT * FROM PRODUTOS"

dados = pd.read_sql(script, conexao)


# AGRUPANDO OS DADOS  

forn_por_qtd = dados.groupby("FORNECEDOR")["QTDPROD"].sum().reset_index()
forn_por_vlr = dados.groupby("FORNECEDOR")["VLRPROD"].sum().reset_index()
nome_por_qtd = dados.groupby("NOMEPROD")["QTDPROD"].sum().reset_index()


# CRIANDO GRÁFICOS 

fig_forn_por_qtd = px.bar(forn_por_qtd, x="FORNECEDOR", 
                          y="QTDPROD", color="FORNECEDOR")
fig_forn_por_qtd.update_layout(template="plotly_dark")

fig_forn_por_vlr = px.pie(forn_por_vlr, names="FORNECEDOR", 
                          values="VLRPROD", hole=0.5)
fig_forn_por_vlr.update_layout(template="plotly_dark")

fig_nome_por_qtd = px.area(nome_por_qtd, x="NOMEPROD", y="QTDPROD", color="NOMEPROD")
fig_nome_por_qtd.update_layout(template="plotly_dark")


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    
    # ✅ TÍTULO CENTRALIZADO
    html.H1("Dashboard de Produtos e Fornecedores", style={
        "textAlign": "center",
        "marginTop": "20px",
        "marginBottom": "40px",
        "color": "white"
    }),
    
   dbc.Row([
    dbc.Col(
        dcc.Dropdown(
            id="dropdown-selecao",
            options=[{"label": i, "value": i}
                     for i in dados["FORNECEDOR"].unique()],
            multi=True,
            className="dbc",
            style={"background": "#222", "color": "#000"}
        ),
        width=4  # Corrigido aqui
    ),
]),


    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig_forn_por_qtd)], width=4),
        dbc.Col([dcc.Graph(figure=fig_forn_por_vlr)], width=4)
    ], className="mb-3"),
    
    dbc.Row([dcc.Graph(figure=fig_nome_por_qtd)]),
    dbc.Row(id="teste")
    
])


@app.callback(
    Output("fig_forn_por_qtd", "figure"),
    Input("dropdown-selecao", "value")
    )

def atualiza_dash(fornecedores):
    dados_forn = dados[dados["FORNECEDOR"].isin(fornecedores)]
    forn_por_qtd = dados_forn.groupby("FORNECEDOR")["QTDPROD"] .sum().reset.index()
    
    fig_forn_por_qtd = px.bar(forn_por_qtd, x="FORNECEDOR",
                              y="QTDPROD", color="FORNECEDOR")
    
    fig_forn_por_qtd.update_layout(template="plotly_dark", showlegend=False)
    
    return fig_forn_por_qtd
    








if __name__ == "__main__":
    app.run(debug=True, port=8050)
