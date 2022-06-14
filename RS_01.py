from refraccion_sismica import *

#data = data_reading("registro_1.txt")
#print(data)

#initial_plot(data)
#Z_1 = data_processing(data, [90], "velocities")
#print(Z_1)

data_1 = data_reading("registro_A.txt")
data_2 = data_reading("registro_B_ordenado.txt")

#print(data_processing(data_1, [90], "velocities"))
#print(data_processing(data_2, [45], "velocities"))

redpath_data = redpath_method(data_1, data_2, [90], [45], "plot")
