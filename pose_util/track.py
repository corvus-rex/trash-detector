def track_objects(C1, C2):
    matches = {}  # To store mappings of {centroid_in_C1: centroid_in_C2}
    used = set()  # To keep track of matched centroids in C2

    for c1 in C1:
        # Compute distances from c1 to all centroids in C2
        distances = [(c2, euclidean_distance(c1, c2)) for c2 in C2 if c2 not in used]
        if distances:
            # Find the closest centroid in C2
            closest_c2, _ = min(distances, key=lambda x: x[1])
            matches[c1] = closest_c2
            used.add(closest_c2)

    # Optionally handle unmatched centroids
    unmatched_in_C1 = set(C1) - set(matches.keys())
    unmatched_in_C2 = set(C2) - used

    return matches, unmatched_in_C1, unmatched_in_C2

def euclidean_distance(c1, c2):
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)**0.5
