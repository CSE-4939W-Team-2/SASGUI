import pandas as pd
import numpy as np
q = np.loadtxt('q_200.txt', dtype=str, delimiter=',')
indf = pd.DataFrame(pd.read_csv("example_curve.csv"))
spec = np.log10(np.array(indf.loc[:,q])+1.)
print(spec)