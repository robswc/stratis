from typing import List

from loguru import logger

from components.positions import Position


def remove_overlapping_positions(positions: List[Position], max_overlap: int = 1):
    """Remove overlapping positions from a list of positions."""
    logger.debug(f'Removing overlapping positions (max overlap: {max_overlap})...')
    new_positions = []

    # Sort the positions by their opened timestamp
    sorted_positions = sorted(positions, key=lambda x: x.opened_timestamp)

    i = 0
    last_timestamp = None
    while i < len(sorted_positions):
        p = sorted_positions[i]
        if last_timestamp is None:
            last_timestamp = p.closed_timestamp
            new_positions.append(p)
            i += 1
            continue

        no_overlap = last_timestamp < p.opened_timestamp
        if no_overlap:
            new_positions.append(p)
            last_timestamp = p.closed_timestamp

        i += 1

    # Return the modified copy of the list
    logger.debug(f'Removed {len(positions) - len(new_positions)} overlapping positions. (max overlap: {max_overlap})')
    return new_positions
