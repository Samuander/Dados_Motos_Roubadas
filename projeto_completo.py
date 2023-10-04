import folium
from folium import plugins
from folium import Popup
import geopandas as gpd
from folium.plugins import Search
import json

LOCAIS = gpd.read_file('SHAPES/LOCAIS_rou_rec_MOTOS.shp')
LOCAIS.head(5)

SETOR_CENSITÁRIO = gpd.read_file('SHAPES/PI_Setores_2021_TERESINA.shp')
SETOR_CENSITÁRIO.head(5)

PIAUI = gpd.read_file('SHAPES/PIAUI.shp')
PIAUI.head(5)


#CRIANDO MAPA FOLIUM (OK)-----------------------------------------------------------
mapa = folium.Map(
    location=[-7.1502,-42.2685],
    zoom_start=6
)


#--------------PAREI AQUI
# 
# REPOSITÓRIO DE MAPAS BASE
#https://leaflet-extras.github.io/leaflet-providers/preview/

fg = folium.FeatureGroup(control=False)
mapa.add_child(fg)

g1 = plugins.FeatureGroupSubGroup(fg,'Locais de Roubo de Moto')
mapa.add_child(g1)
g2 = plugins.FeatureGroupSubGroup(fg,'Setores Censitários')
mapa.add_child(g2)
g3 = plugins.FeatureGroupSubGroup(fg,'Municípios do Piauí')
mapa.add_child(g3)

#ADICIONANDO CAMADAS DO MAPS E STREETVIEW (OK)--------------------------------------
folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='google',
    name='google maps',
    max_zoom=20,
    subdomains=['mt0', 'mt1','mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(mapa)

folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='google',
    name='google street view',
    max_zoom=20,
    subdomains=['mt0', 'mt1','mt2', 'mt3'],
    overlay=False,
    controla=True,
).add_to(mapa)

folium.raster_layers.TileLayer('CartoDB Positron').add_to(mapa)


#CRIANDO ESTILOS PARA APLICAR NOS GEOJSON
def sf_regfund(feature):
    return{
        'color': 'red',
        'weight': 1,
        'fillOpacity': 0.1
    }

def sf_regfund_base(feature):
    return{
        'color': 'red',
        'weight': 0.1,
        'fillOpacity': 0
    }

def pi_base (feature):
    return{
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.02
    }

#TENTATIVA 02 --------- (OK)---- substitui o primeiro geojson criado------------------

# for index, row in REGFUND.iterrows():

from folium.plugins import FastMarkerCluster


# Criando a camada de pontos com FastMarkerCluster
locais_search = FastMarkerCluster(
    LOCAIS[['ed_latitud', 'ed_longitu']],
    name='Locais de Roubo de Moto',
    # control=False,
    popups=[folium.Popup(f"<b>Número do BO:</b> <code>{nr_reg}</code> <br>", max_width=300) 
            for nr_reg in LOCAIS['NR_REG']]
)


# Adicione a camada de pontos à subcamada g1
locais_search.add_to(g1)

setcens = folium.GeoJson(
    SETOR_CENSITÁRIO,name='setcensi',control=False,style_function=sf_regfund,    
    # style_function=sf_regfund,
    )

pi_search = folium.GeoJson(
    PIAUI,name='pisearch',control=False,style_function=pi_base,) 
#     folium.Popup("""IMÓVEL: {} <br>
#     PROC. SEI: {}
#     """.format(row.PROPRIEDAD,
#     str(row.SEI)),
#     max_width=300).add_to(regfolium)


setcens.add_to(g2)
pi_search.add_to(g3)

#CRIANDO CAMPOS DE BUSCA

# plugins.Search(regfolium, search_zoom=13, geom_type='Polygon',search_label='PROPRIEDAD').add_to(mapa)

statesearch = Search(
    layer = locais_search,
    geom_type="Point",
    placeholder="Pesquisar BO",
    collapsed=True,
    search_label="NR_REG",).add_to(mapa)

statesearch = Search(
    layer = pi_search,
    geom_type="Polygon",
    placeholder="Pesquisar Município",
    collapsed=True,
    search_label="NM_MUN").add_to(mapa)


#DIVISÃO DO PI NO MAPA (OK)--------------------------------------------------------

for index, municipio in PIAUI.iterrows():
    municipio_geojson = folium.GeoJson(municipio.geometry,name='pi',
        style_function= pi_base)

    ttype = folium.Tooltip("""
            {} <br>
            """.format(municipio.NM_MUN))

    ttype.add_to(municipio_geojson)
    # mapa.add_child(municipio_geojson)
    municipio_geojson.add_to(g3)

#BARRA ORGANIZADORA DE CAMADAS (OK)----------------------------------------------------------------
# plugins.Search(piaui, search_zoom=6, geom_type='Polygon').add_to(mapa)
l= folium.LayerControl().add_to(mapa)

#EXPORTAR RESULTADO COMO HTML (OK)----------------------------------------------------------------
mapa.save('PROJ.PRINCIPAL.html')
mapa