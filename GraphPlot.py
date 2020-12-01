#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "pressure", help='Enter the path where reading are saved')
args = parser.parse_args()

# In[2]:



data = pd.read_csv(str(args.pressure),header=None)


# In[74]:

print('Average Force',np.average(data[0]))
print('Average Pressure',np.average(data[1]))

plt.plot(data[0],data[1])
plt.xlabel('Force (N)')
plt.ylabel('Pressure (Kpa)')
plt.grid()
plt.show()

