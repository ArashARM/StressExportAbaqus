from odbAccess import openOdb
import os
import shutil
import math
import numpy as np

output_file = 'RD.txt'
def calculate_element_centroid(instance, connected_nodes):

    node_coordinates = np.array([instance.nodes[node_idx - 1].coordinates for node_idx in connected_nodes])
    centroid = np.mean(node_coordinates, axis=0)  # Compute mean (average) for each coordinate
    return tuple(centroid)

def extract_stress_data(odb, instance_name, step_name='Step-1'):
  
    field_output = odb.steps[step_name].frames[-1].fieldOutputs['S']
    instance = odb.rootAssembly.instances[instance_name]
    field = field_output.getSubset(region=instance, position=CENTROID)
    field_values = field.values

    results = []
    for value in field_values:
        stress_data = {
            'element_label': instance.elements[value.elementLabel - 1].label,
            'stress': value.data,  # Stress tensor components (S11, S22, S33, S12, S13, S23)
        }
        connected_nodes = instance.elements[value.elementLabel - 1].connectivity
        centroid_coords = calculate_element_centroid(instance, connected_nodes)
        results.append({**stress_data, **dict(zip(['S11', 'S22', 'S33', 'S12', 'S13', 'S23'], stress_data['stress'])), **dict(zip(['Centroid_X', 'Centroid_Y', 'Centroid_Z'], centroid_coords))})

    return results

def write_results_to_file(results, file_path):

    with open(file_path, 'w') as sortie:
        for result in results:
            sortie.write(','.join([str(value) for value in result.values()]) + '\n')

def main():
    odb_name = 'Job-1'  # ODB name
    odb_path = './'  # ODB file path
    my_odb_path = os.path.join(odb_path, odb_name + '.odb')

    # Open ODB file
    odb = openOdb(my_odb_path)

    # Get instance names from the ODB
    for instance_name in odb.rootAssembly.instances.keys():
        print(instance_name)

    # Extract stress data and element centroids
    instance_name = 'PART-1-1'
    results = extract_stress_data(odb, instance_name)

    # Write results to the file
    write_results_to_file(results, output_file)

    # Close ODB file
    odb.close()

if __name__ == "__main__":
    main()
