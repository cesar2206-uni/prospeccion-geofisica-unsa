import numpy as np
import matplotlib.pyplot as plt

def wavefront_procedure(x_left, x_right, ratio):
    """
    The wavefront method, based in the x vector of results in each dt, for the second velocity line obtained in the linear regression
    """
    x_left = np.array(x_left)
    x_right = np.array(x_right)

    L_left = np.array([x_left[i+1] - x_left[i] for i in range(len(x_left)-1)])
    L_right= np.array([x_right[i+1] - x_right[i] for i in range(len(x_right)-1)])

    m_left = -np.tan(np.arcsin(ratio/L_left)) # Slope of the line
    m_right = np.tan(np.arcsin(ratio/L_right)) # Slope of the line
    b_left = -m_left * x_left[:-1]
    b_right = -m_right * x_right[1:]
#    for i in range(len(m_left)):  
#        plt.plot(np.arange(0, 70, 1), m_left[i] * np.arange(0, 70, 1) + b_left[i])
#        plt.plot(np.arange(0, 70, 1), m_right[i] * np.arange(0, 70, 1) + b_right[i])
#   plt.show()
    x_1 = - (b_left - b_right)/(m_left - m_right)
    y_1 = m_left * x_1 + b_left
    return np.array([x_1, y_1]).T

print(wavefront_procedure([0, 10, 20], [50, 60, 70], 5))
