# Obtención de velocidades a través del ensayo de refracción sismica
# Autor: César Sánchez

## Librerias
from pandas import DataFrame, read_csv
import plotly.graph_objects as go
from numpy import split, where, array, reshape, arange, cos, arcsin, repeat, tan
from sklearn import linear_model

## Entrada de datos

def data_reading(path):
    """
    This function with the path of the .txt, create a dataframe with the values
    """
    data = read_csv(path ,skiprows = 1, sep = "\t", header = None, names = ["x", "t"])
    return data

def initial_plot(data):
    """
    This function plot a scatter plot of the data, to choose the data for each regression  
    """    
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
    return 0

def special_split(arr, separation_values):
    """
    Function to split a list
    """
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

def data_processing(data, inflexion_points, results = "plot"):
    """
    This function is the principal to process data of seismic refaction:
    data = dataframe of the seismic refraction data
    inflexion_points = a list of the points with change of the slope, for example : [106], specifically of the distance
    results: a string which select the type of results
    """
    ## Initial scatter plot
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
    if results == "plot":
        fig.show()
    else:
        pass
    # Transformation of dataframe in array
    x = data["x"].to_numpy()
    y = data["t"].to_numpy()

    # Inflexion points
    x_separation_values = inflexion_points
    y_separation_values = [y[where(x == value)] for value in
                       x_separation_values]

    # Searching the slopes changes
    ## Linear regresion

    X = special_split(x, x_separation_values)
    Y = special_split(y, y_separation_values)

    regression_results, velocities, intersections = [], [], []

    for i in range(len(X)):
    
        ## Velocities 
        reg = linear_model.LinearRegression()
        X_1 = reshape(X[i],(-1, 1))
        reg.fit(X_1, Y[i])
        regression_results.append([reg.coef_, reg.intercept_, reg.score(X_1, Y[i])])
        velocities.append(1 / reg.coef_)
    
        ## Intersections in linear regressions
        if i > 0:
            reg_previous = linear_model.LinearRegression()
            X_2 = reshape(X[i-1],(-1, 1))
            reg_previous.fit(X_2, Y[i-1])
            intersections.append(-(reg_previous.intercept_ - reg.intercept_) / (reg_previous.coef_ - reg.coef_))
    
            ## Linear regression ploting
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

    # Soil Thicknesses
    Z = []
    for i in range(len(x_separation_values)):
        t_i = regression_results[i+1][1]
        Z.append(t_i * velocities[i] * velocities[i+1] / (2 * ((velocities[i+1] ** 2 - velocities[i] ** 2)**0.5)))

    fig.update_layout(xaxis_title = "Distancia de la fuente (m)",
                      yaxis_title = "Tiempo de viaje (ms)",
                      title = "Ensayo de Refracción Sísmica - Dromocrona registrada",
                      font = dict(size = 18)
                      ) 
    # Results
    if results == "plot":
        fig.show()
        return 0
    
    elif results == "thickness":
        return Z
    
    elif results == "velocities":
        return velocities
    
    elif results == "regression_results":
        return regression_results
    
    elif results == "critical_distances":
        return intersections

    else:
        return 0

def redpath_method(data_1, data_2, inflexion_1, inflexion_2, result = "table"):
    """
    Function of the redpath method to obtain the thicknesses of all the line with geophones
    The data_2 is the domocronic of the right side
    results = {table, plot}
    """
    # Data reading
    redpath_data = DataFrame()
    redpath_data["x_1"] = data_1["x"]
    redpath_data["x_2"] = data_2[::-1].reset_index(drop = True)["x"]
    
    # Regresion results and velocities
    reg_res_1 = data_processing(data_1, inflexion_1, "regression_results")
    reg_res_2 = data_processing(data_2, inflexion_2, "regression_results")
    V_A = data_processing(data_1, inflexion_1, "velocities")
    V_B = data_processing(data_2, inflexion_2, "velocities")
    V_1 = (V_A[0] + V_B[0])/2
    i_c = 0.5 * (arcsin(V_1/V_A[1]) + arcsin(V_1/V_B[1]))

    # Interpolation with the regressions
    redpath_data["T_D1"] = redpath_data["x_1"] * reg_res_1[1][0] + reg_res_1[1][1]
    redpath_data["T_D2"] = redpath_data["x_2"] * reg_res_2[1][0] + reg_res_2[1][1]
    
    # Verification 
    if max(data_1["t"]) == max(data_2["t"]):
        T_t = max(data_1["t"])
    else:
        print("T_t is'nt correct, check the last geophone departure tim")
        return 0

    # Redpath Method
    redpath_data["dT"] = 0.5 * (redpath_data["T_D1"] + redpath_data["T_D2"] - T_t)
    redpath_data["Zd"] = redpath_data["dT"] * V_1 / cos(i_c)

    # Plot processing
    X = redpath_data["x_1"].to_numpy()
    Y_surface = repeat(0, len(X))
    Y_redpath = redpath_data["Zd"]

    # Results
    if result == "table":
        return redpath_data
    elif result == "plot":
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x = X, y = Y_surface,
                       mode = "lines",
                       name = "Superficie"
            )
        )
        
        fig.add_trace(
            go.Scatter(x = X, y = Y_redpath,
                       mode = "lines",
                       name = "Estrato 1"
            )
        )
        fig.update_layout(xaxis_title = "Distancia (m)",
                      yaxis_title = "Profundidad (m)",
                      title = "Ensayo de Refracción Sísmica - Método de Redpath",
                      font = dict(size = 18)
                      ) 
        fig.update_yaxes(autorange="reversed")
        fig.show()
        return 0
    else:
        print("Incorrect results value")
        return 0

def wavefront_procedure(x_left, x_right, ratio):
    """
    The wavefront method, based in the x vector of results in each dt, for the second velocity line obtained in the linear regression
    """
    x_left = array(x_left)
    x_right = array(x_right)

    L_left = array([x_left[i+1] - x_left[i] for i in range(len(x_left)-1)])
    L_right= array([x_right[i+1] - x_right[i] for i in range(len(x_right)-1)])

    m_left = -tan(arcsin(ratio/L_left)) # Slope of the line
    m_right = tan(arcsin(ratio/L_right)) # Slope of the line
    b_left = -m_left * x_left[:-1]
    b_right = -m_right * x_right[1:]
#    for i in range(len(m_left)):  
#        plt.plot(np.arange(0, 70, 1), m_left[i] * np.arange(0, 70, 1) + b_left[i])
#        plt.plot(np.arange(0, 70, 1), m_right[i] * np.arange(0, 70, 1) + b_right[i])
#   plt.show()
    x_1 = - (b_left - b_right)/(m_left - m_right)
    y_1 = m_left * x_1 + b_left
    return array([x_1, y_1]).T


def wavefront_method(data_1, data_2, inflexion_1, inflexion_2, result = "table"):
    """
    Function of the wavefront method to obtain the second velocitie
    The data_2 is the domocronic of the right side
    results = {table, plot}
    """
    dt = 10 # ms
    # Velocity in the first soil layer
    V_A = data_processing(data_1, inflexion_1, "velocities")
    V_B = data_processing(data_2, inflexion_2, "velocities")
    V_1 = (V_A[0] + V_B[0])/2
    
    R = V_1 * dt # V in m/ms and dt in ms
    
    # Regresion results
    reg_res_1 = data_processing(data_1, inflexion_1, "regression_results")
    reg_res_2 = data_processing(data_2, inflexion_2, "regression_results")
    
    # Selection of points
    
    t_1 = data_1["t"].iloc[1]
    t_2 = data_2["t"].iloc[-2:-1]
    
    t1_values = array([t_1, t_1 + dt, t_1 + 2 * dt])
    t2_values = array([t_2 - 2 * dt, t_2 - dt, t_2])
    print(t1_values, t2_values)

    left_values = (t1_values - reg_res_1[1][1]) / reg_res_1[1][0]
    right_values = (t2_values - reg_res_2[1][1]) / reg_res_2[1][0] 
    print(left_values, right_values)
    
    # Result of intersections
    XY = wavefront_procedure(left_values, right_values, R)
    
    # 2nd Velocitie obtained
    V_2 = (XY[1][0] - XY[0][0])/10
    return XY
    
