# Obtención de velocidades a través del ensayo de refracción sismica
# Autor: César Sánchez

## Librerias
from pandas import DataFrame, read_csv
import plotly.graph_objects as go
from numpy import split, where, array, reshape, arange

## Entrada de datos

data = read_csv("registro_2.txt",skiprows = 1, sep = "\t", header = None, names = ["x", "t"])
print(data)
x = data["x"].to_numpy()
y = data["t"].to_numpy()

## Ploteo inicial
fig = go.Figure()
fig.add_trace(go.Scatter(x = data["x"], y = data["t"],
                         mode = "markers",
                         name = "Puntos registrados"
))

fig.update_layout(xaxis_title = "Distancia de la fuente (m)",
                  yaxis_title = "Tiempo de viaje (ms)",
                  title = "Ensayo de Refracción Sísmica - Dromocrona registrada",
                  font = dict(size = 18)
                  ) 
fig.show()

## Puntos de Inflexión
x_separation_values = [2]
y_separation_values = [y[where(x == value)] for value in x_separation_values]

## Busqueda de los cambios de pendiente
def special_split(arr, separation_values):
    separated_list =[]
    for i, value in enumerate(separation_values):
        if i == 0: 
            separated_list.append(arr[arr<=value])
            separated_list.append(arr[arr>value])
        else:
            l_inf = separated_list[-1][separated_list[-1]<=value]
            l_sup = separated_list[-1][separated_list[-1]>value]
            separated_list = separated_list[:-1]
            separated_list.append(l_inf)
            separated_list.append(l_sup)
    return separated_list

## Regresiones lineales
from sklearn import linear_model

X = special_split(x, x_separation_values)
Y = special_split(y, y_separation_values)

regression_results, velocities, intersections = [], [], []

for i in range(len(X)):
    
    # Obtención de Velocidades
    reg = linear_model.LinearRegression()
    X_1 = reshape(X[i],(-1, 1))
    reg.fit(X_1, Y[i])
    regression_results.append([reg.coef_, reg.intercept_, reg.score(X_1, Y[i])])
    velocities.append(1 / reg.coef_)
    
    # Obtención de Intersecciones
    if i > 0:
        reg_previous = linear_model.LinearRegression()
        X_2 = reshape(X[i-1],(-1, 1))
        reg_previous.fit(X_2, Y[i-1])
        intersections.append(-(reg_previous.intercept_ - reg.intercept_) / (reg_previous.coef_ - reg.coef_))
    
        # Ploteo de las regresiones lineales
        if i == 1:
            Y_pred_0 = reg_previous.predict(reshape(arange(X[i-1][0], intersections[i-1], 0.1),(-1, 1)))
            fig.add_trace(go.Scatter(x = arange(X[i-1][0], intersections[i-1], 0.1), y = Y_pred_0,
                             mode = "lines",
                             name = "Estrato 1"))

            Y_pred_1 = reg.predict(reshape(arange(intersections[i-1], X[i][-1], 0.1),(-1, 1)))
            fig.add_trace(go.Scatter(x = arange(intersections[i-1],X[i][-1], 0.1), y = Y_pred_1,
                             mode = "lines",
                             name = "Estrato 2"))
        else:
            Y_pred_i = reg.predict(reshape(arange(intersections[i-1], X[i][-1], 0.1),(-1, 1)))
            fig.add_trace(go.Scatter(x = arange(intersections[i-1],X[i][-1], 0.1), y = Y_pred_i,
                             mode = "lines",
                             name = "Estrato "+str(i+1)))
fig.update_layout(xaxis_title = "Distancia de la fuente (m)",
                  yaxis_title = "Tiempo de viaje (ms)",
                  title = "Ensayo de Refracción Sísmica - Dromocrona registrada",
                  font = dict(size = 18)
                  ) 
fig.show()

## Cálculo de espesores
Z = []
for i in range(len(x_separation_values)):
    t_i = regression_results[i+1][1]
    Z.append(t_i * velocities[i] * velocities[i+1] / (2 * ((velocities[i+1] ** 2 - velocities[i] ** 2)**0.5)))

fig.update_layout(xaxis_title = "Distancia de la fuente (m)",
                  yaxis_title = "Tiempo de viaje (ms)",
                  title = "Ensayo de Refracción Sísmica - Dromocrona registrada",
                  font = dict(size = 18)
                  ) 
## Resultados

print("Espesores")
print(Z)

print("Velocidades")
print(velocities)

print("Resultados de la regresión [a, b, R2]")
print(regression_results)

print("Distancias críticas")
print(intersections)




