from components.positions import Position


def remove_overlapping_positions(positions: Position, max_overlap):
    positions_copy = positions[:]

    # Iterate over the positions, comparing each one to all subsequent positions
    for i in range(len(positions_copy)):
        num_overlaps = 0
        for j in range(i + 1, len(positions_copy)):
            position_i = positions_copy[i]
            position_j = positions_copy[j]

            # Check if the positions overlap
            i_start = position_i.opened_timestamp
            i_end = position_i.closed_timestamp
            j_start = position_j.opened_timestamp
            j_end = position_j.closed_timestamp
            if (i_start <= j_end) and (j_start <= i_end):
                num_overlaps += 1  # Increment the overlap counter
                if num_overlaps > max_overlap:
                    positions_copy.pop(j)
                    break

    # Return the modified copy of the list
    return positions_copy
