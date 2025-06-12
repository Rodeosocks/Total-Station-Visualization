import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read in data
column_names = ['FS_number', 'material', 'x', 'y', 'z']
df = pd.read_csv(
    r'Total-Station-Visualization\Site 180 EU3.txt', 
    sep='\s', 
    header=None, 
    comment='#',
    skiprows=7,
    names=column_names
)
datum = pd.read_csv(
    r'Total-Station-Visualization\Site 180 EU3.txt', 
    sep='\s', 
    header=None, 
    nrows=1
)
datum = datum.iloc[0, 1:4].to_numpy()

# Record outlier rows, delete them before plotting
mask = df['x'] > 1000
bad_rows = df[mask].index
print("\n--- Rows to be Deleted (where 'x' > 1000) ---")
if not bad_rows.empty:
    print(f"Row indices to be dropped: {np.array(bad_rows.tolist()) + 8}")
else:
    print("No rows found with 'x' > 1000.")
df = df.drop(bad_rows)

# Sort data into material types and coordinates, shift coords by datum
data_by_material = {}
for name, group_df in df.groupby('material'):
    coords_df = group_df.select_dtypes(include=np.number)
    data_by_material[name] = coords_df.to_numpy() - datum

# Plot results
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# str1 = 'B'
# str2 = 'DB'
# ax.scatter(data_by_material[str1][:, 0], data_by_material[str1][:, 1], data_by_material[str1][:, 2], marker='.')
# ax.scatter(data_by_material[str2][:, 0], data_by_material[str2][:, 1], data_by_material[str2][:, 2])

materials = []
for key in data_by_material:
    ax.scatter(data_by_material[key][:, 0], data_by_material[key][:, 1], data_by_material[key][:, 2], marker='.')
    materials.append(key)

ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Total Station Visualization')
ax.legend(materials)

plt.show()