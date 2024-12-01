import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
with open(r'C:\Code\Projekti2024Syksy\Laptop\tcp\sensor_values.csv', mode='r') as file:
    reader = csv.DictReader(file)  
    
    
    points = []
    
    
    for row in reader:
        points.append((float(row['x_value']), float(row['y_value']), float(row['z_value'])))

    points2 =np.array(points)

print(points2[0])

def randomCenterPoints(points2):

    
    min_x = min(points2[:, 0])
    max_x = max(points2[:, 0])
    print(f"min_x: {min_x}, max_x: {max_x}")
    
    min_y = min(points2[:, 1])
    max_y = max(points2[:, 1])
    print(f"min_y: {min_y}, max_y: {max_y}")
    
    min_z = min(points2[:, 2])
    max_z = max(points2[:, 2])
    print(f"min_z: {min_z}, max_z: {max_z}")
    random_points = np.column_stack((
    np.random.uniform(min_x, max_x, 6),  
    np.random.uniform(min_y, max_y, 6), 
    np.random.uniform(min_z, max_z, 6)   
    ))
    centerPoints= np.array(random_points)
    print("CenterPoints:")
    print(centerPoints)
    return centerPoints

def countDistanceBetweenPoints(p1,p2):

    return np.sqrt(np.sum((p1-p2)**2))



def groupingPoints(center_points):
    for iteration in range(100):  # Iterate for a maximum of 100 iterations
        print(f"Iteration {iteration + 1}")
        groups = {i: [] for i in range(len(center_points))}  # Create empty groups for each center
        
        # Assign each point to the nearest center
        for i in range(len(points2)):
            point = points2[i]
            distances = [countDistanceBetweenPoints(point, center_point) for center_point in center_points]
            closest_center = np.argmin(distances)  # Find the closest center
            groups[closest_center].append(point)
        
        # Check for empty groups and reinitialize centroids if necessary
        empty_centers = [center_idx for center_idx, group in groups.items() if len(group) == 0]
        if empty_centers:
            print(f"Centers {empty_centers} had no points assigned. Reinitializing all centroids.")
            
            # Reinitialize all centroids to random values
            center_points = randomCenterPoints(points2)
        else:
            # Update centroids
            new_centers = []
            for center_idx, group in groups.items():
                if len(group) > 0:  # Only update centroids with assigned points
                    new_center = np.sum(group, axis=0) / len(group)  # Calculate the new center as the mean of the group
                    new_centers.append(new_center)
            
            center_points = np.array(new_centers)

    return groups, center_points
'''
def generate_header_file(centroids, filename="centroids.h"):
    # Find the min and max values for each coordinate (x, y, z)
    min_x, max_x = min(centroids[:, 0]), max(centroids[:, 0])
    min_y, max_y = min(centroids[:, 1]), max(centroids[:, 1])
    min_z, max_z = min(centroids[:, 2]), max(centroids[:, 2])

    # Create the header file
    with open(filename, 'w') as f:
        # Write the header guard
        f.write("#ifndef CENTROIDS_H\n")
        f.write("#define CENTROIDS_H\n\n")

        # Write the centroids array
        f.write("float centroids[6][3] = {\n")
        
        # Row 1: [min_x, 0, 0]
        f.write(f"    {{ {min_x}, 0.0, 0.0 }},\n")
        # Row 2: [max_x, 0, 0]
        f.write(f"    {{ {max_x}, 0.0, 0.0 }},\n")
        # Row 3: [0, min_y, 0]
        f.write(f"    {{ 0.0, {min_y}, 0.0 }},\n")
        # Row 4: [0, max_y, 0]
        f.write(f"    {{ 0.0, {max_y}, 0.0 }},\n")
        # Row 5: [0, 0, min_z]
        f.write(f"    {{ 0.0, 0.0, {min_z} }},\n")
        # Row 6: [0, 0, max_z]
        f.write(f"    {{ 0.0, 0.0, {max_z} }}\n")
        
        # Close the array and the header guard
        f.write("};\n\n")
        f.write("#endif  // CENTROIDS_H\n")

    print(f"Header file '{filename}' generated successfully.")'''

center_points= randomCenterPoints(points2)
grouped_points, new_center_points = groupingPoints(center_points)


for center_idx, group in grouped_points.items():
    print(f"Group {center_idx}: {len(group)} points")

print("New center points:")
print(new_center_points)
#generate_header_file(new_center_points)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


colors = ['r', 'g', 'b', 'y', 'c', 'm']
for center_idx, group in grouped_points.items():
    group = np.array(group)
    ax.scatter(group[:, 0], group[:, 1], group[:, 2], c=colors[center_idx % len(colors)], label=f"Group {center_idx}")


new_center_points = np.array(new_center_points)
ax.scatter(new_center_points[:, 0], new_center_points[:, 1], new_center_points[:, 2], c='k', marker='x', label="New Centers")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()


