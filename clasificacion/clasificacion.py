from table_dicts import *
import plotly.graph_objects as go

list_dicts = [ASTM_D5777, US_ArmyCorps_1995, Livemore_California_1973, Geoconsult_Valencia_2001, UniversidadValle_Cali_2001, InstitutoMexicanoTransporte_2003, WDCSHGR_Japon_1979]
V_p = 1200

matches = []
for dict_item in list_dicts:
    dict_match = []
    for key, value in dict_item.items():
        if len(value) == 1:
            if V_p == value[0]:
                dict_match.append(key + " - Vp (" + str(value[0]) + ")")
            elif V_p >= value[0] * 0.9 and V_p <= value[0] * 1.1:
                dict_match.append(key + " (Aproximadamente)" + " - Vp ("+ str(value[0])+ ")")
            else:
                pass
        else:
            if V_p >= value[0] and V_p <= value[1]:
                dict_match.append(key + " - Vp (" + str(value[0]) + "-"+ str(value[1])+")")
            else:
                pass
    matches.append(dict_match)

match = [" <br>".join(element) for element in matches]
match = ["No entra en los rangos de clasificación" if element == '' else element for element in match]

values = [['"Standard Guide for Using the Seismic Refraction Method for Subsurface Investigation" - NORMA ASTM D 5777', '"Geophysical Exploration for Engineering and Environmental Investigations" U.S.Army Corps of Engineers. Washington D.C. August 1995','Bruce Redpath. "Seismic Refraction Exploration for Engineering Site Investigations". Explosive Excavation Research Laboratory Livemore, California U.S.A 1973','Rodríguez Manuel Arlandi "Geofisica Aplicada a la Obra Civil. Método Geoeléctrico y Sísmica de Refracción. Casos Prácticos" Geoconsult Ingenieros Consultores. Valencia, España. 2001', '"Tesis sobre el Comportamiento Sísmico de los Depósitos de Suelos del Área de Cañaveralejo, Cali, Colombia". Unicersidad del Valle, Cali, Colombia. 2001','"Geofisica Aplicada en los Proyecto Básicos de Ingeniería Civil". Instituto Mexicano de Tranporte, 2003','"Manual of Seismological Observatory Practice", World Data Center for Solid Herat Geophysics Report SE-20, Japón, 1979'], match]

fig = go.Figure(data=[go.Table(
  columnorder = [1,2],
  columnwidth = [200,200],
  header = dict(
    values = [['<b>Referencias Bibliográficas</b>'],
                  ['<b>Descripción del estrato</b>']],
    line_color='darkslategray',
    fill_color='royalblue',
    align=['left','left'],
    font=dict(color='white', size=12),
    height=40
  ),
  cells=dict(
    values=values,
    line_color='darkslategray',
    fill=dict(color=['paleturquoise', 'white']),
    align=['left', 'left'],
    font_size=12,
    height=30)
    )
])
fig.show()

