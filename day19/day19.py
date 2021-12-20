import itertools
from collections import defaultdict


coords_per_scanner = {}

with open('input') as f:
    scanner = -1
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n')
        if not line:
            continue
        if line.startswith('---'):
            scanner += 1
        else:
            if scanner not in coords_per_scanner:
                coords_per_scanner[scanner] = []
            coords_per_scanner[scanner].append(tuple(map(int, line.split(','))))

beacon_at_vector = {}
for scanner, coords in coords_per_scanner.items():
    vectors_for_scanner = {}
    for beacon_pair in itertools.combinations(coords, 2):
        vector_1 = tuple(beacon_pair[0][i] - beacon_pair[1][i] for i in range(3))
        vector_2 = (-vector_1[0], -vector_1[1], -vector_1[2])
        # Assume that each vector is unique in the space
        assert vector_1 not in vectors_for_scanner
        assert vector_2 not in vectors_for_scanner
        vectors_for_scanner[vector_1] = beacon_pair[1]
        vectors_for_scanner[vector_2] = beacon_pair[0]
    beacon_at_vector[scanner] = vectors_for_scanner


def transform_vector(matrix, vector):
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
        matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2],
    )


transformations = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
    [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
    [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
    [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
    [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
    [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
    [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
    [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
    [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
]     


def transform_vector_set(vectors):
    for transformation in transformations:
        transformed_vectors = {}
        for vector in vectors:
            transformed_vectors[transform_vector(transformation, vector)] = vector
        yield transformed_vectors, transformation


def find_transformation_for_new_space(current_space, new_space):
    for transformed_space, transformation in transform_vector_set(new_space):
        if len(current_space & set(transformed_space.keys())) >= 12 * 11:
            return transformed_space, transformation
    return None, None

current_beacons_at_vectors = beacon_at_vector[0].copy()
scanners_to_overlap = list(i for i in range(1, max(beacon_at_vector.keys()) + 1))
scanner_locations = set([(0, 0, 0)])
while len(scanners_to_overlap):
    scanner = scanners_to_overlap[0]
    current_vectors = set(current_beacons_at_vectors.keys())
    transformed_space, transformation = find_transformation_for_new_space(current_vectors, beacon_at_vector[scanner].keys())
    if transformation is None:
        scanners_to_overlap = scanners_to_overlap[1:] + [scanner]
        continue
    else:
        scanners_to_overlap = scanners_to_overlap[1:]
    overlapping_vectors = current_vectors & set(transformed_space.keys())
    scanner_location = None
    for vector in overlapping_vectors:
        orig_vector = transformed_space[vector]
        orig_beacon = beacon_at_vector[scanner][orig_vector]
        scanner_to_beacon = transform_vector(transformation, orig_beacon)
        origin_to_beacon = current_beacons_at_vectors[vector]
        origin_to_scanner = tuple(origin_to_beacon[i] - scanner_to_beacon[i] for i in range(3))
        assert scanner_location is None or origin_to_scanner == scanner_location
        scanner_location = origin_to_scanner
    scanner_locations.add(scanner_location)
    for orig_vector, orig_beacon in beacon_at_vector[scanner].items():
        vector = transform_vector(transformation, orig_vector)
        beacon = transform_vector(transformation, orig_beacon)
        current_beacons_at_vectors[vector] = tuple(scanner_location[i] + beacon[i] for i in range(3))

print(len(set(current_beacons_at_vectors.values())))

max_scanner_distance = 0
for scanner_pair in itertools.combinations(scanner_locations, 2):
    scanner_distance = sum(abs(scanner_pair[0][i] - scanner_pair[1][i]) for i in range(3))
    max_scanner_distance = max(max_scanner_distance, scanner_distance)
print(max_scanner_distance)

