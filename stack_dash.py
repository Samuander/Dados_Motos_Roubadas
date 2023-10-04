import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import HeatMap

LOCAIS = gpd.read_file('SHAPES/LOCAIS_rou_rec_MOTOS.shp')
LOCAIS.head(5)
PIAUI = gpd.read_file('SHAPES/PIAUI.shp')
PIAUI.head(5)

latitude = LOCAIS['ed_latitud']
longitude = LOCAIS['ed_longitu']
localidade = LOCAIS['NR_REG']

mapa = folium.Map(
    location=[-7.1502,-42.2685],
    tiles='cartodbpositron',
    zoom_start=6
)


#------------------FAZER MAPA DE CALOR (fica feio com muitos pontos)
# mapa = folium.Map(location=[-7.1502,-42.2685],zoom_start=6, tiles='Stamen Toner')
# from folium.plugins import HeatMap
# heat_maps = HeatMap(LOCAIS[['ed_latitud', 'ed_longitu']])
# mapa.add_child(heat_maps)

#------------------DIVISÃO DO PI NO MAPA
fmap = folium.Map(tiles = 'cartodbpositron')
limites = folium.features.GeoJson(PIAUI,
 style_function=lambda feature:{
    'color': 'black',
    'weight': 2,
    'fillOpacity': 0.0
 })

#------------------POP UP DENTRO DOS LIMITES DO PI
limites.add_child(folium.Popup(PIAUI.NM_MUN ))

# #TESTE 02 DE POPUP PARA MUNICÍPIOS
# popup = folium.Popup(PIAUI.NM_MUN)

# popup.add_to(limites)

mapa.add_child(limites)

#------------------PONTOS AGRUPADOS
from folium.plugins import FastMarkerCluster

mc = FastMarkerCluster(LOCAIS[['ed_latitud', 'ed_longitu']],
    tooltip='Teste',
    )
mapa.add_child(mc)    
#------------------POPUP PARA PONTOS DSG
mc.add_child(folium.Popup(['NR_REG']))


#------------------ADICIONAR opção de clicar no mapa e exibir as coordenadas
mapa.add_child(folium.LatLngPopup())

#CRIANDO POPUPS E TOOLTIPS
for index, municipio in PIAUI.iterrows():
    municipio_geojson = folium.features.GeoJson(municipio.geometry,
    style_function= lambda feature: {
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.1
    })
    popup = folium.Popup("""
            {} <br>
            """.format(municipio.NM_MUN),
            max_width=300)

    popup.add_to(municipio_geojson)

    ttype = folium.Tooltip("""
            Município: {} <br>
            """.format(municipio.NM_MUN))

    ttype.add_to(municipio_geojson)

    municipio_geojson.add_to(mapa)

    municipio_geojson.add_to(mapa)

mapa.save('heatmap2.html')

mapa