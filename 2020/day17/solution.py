"""
Implement a solution for day 17 that generically handles n-dimensional arrays

The part1/solution.py and part2/solution.py were used for the initial
submission and this was written after the fact to generalize the solution.
"""
import itertools
import numpy as np

import click


def translate_input(input_str):
    """
    Translate an input string of # & . characters to a list of integers

    The mapping is:
    # -> 1
    . -> 0
    """
    out = []
    for character in input_str:
        out.append(1 if character == '#' else 0)
    return out


def read_file(filename):
    """
    Read a file containing list of rows/cols of #/.

    Returns a 2-dimensional list of integers 1/0.
    """

    input_array = []
    # with open('test.txt') as file:
    with open(filename) as file:
        for line in file.readlines():
            input_array.append(translate_input(line.strip()))
    return input_array


def create_ndarray(input_array, ndimensions):
    """
    Expand the 2D input to an n-dimensional array.

    The original input will be centered.
    """

    # 2D input to numpy array 2D
    ndarray = np.array(input_array, dtype='B')

    # Pad the 2D input with rows/columns of zeros
    # ndarray = np.pad(ndarray, ((1, 1), (1, 1)), constant_values=0)

    # Expand the array from 2-dimentions to n-dimensions
    for dim in range(2, ndimensions):
        ndarray = ndarray[np.newaxis, ...]
        pad_width = [(0, 0)]
        pad_width.extend([(0, 0)] * dim)
        pad_width = tuple(pad_width)
        ndarray = np.pad(ndarray, pad_width, constant_values=0)

    return ndarray


def process_ndarray(ndarray):
    """
    Iterate over the elements of an n-dimensional array and set the
    new energy state based on the following rules:

    - If a cube is active and exactly 2 or 3 of its neighbors are also
    active, the cube remains active. Otherwise, the cube becomes inactive.
    - If a cube is inactive but exactly 3 of its neighbors are active,
    the cube becomes active. Otherwise, the cube remains inactive.
    """
    print(f'Processing ndarray with shape {ndarray.shape}')
    new_ndarray = ndarray.copy()

    # Create a list of ranges for each dimension of the ndarray
    ndarray_iter = [range(x) for x in ndarray.shape]

    # Iterate over the elements in the ndarray
    for prod in itertools.product(*ndarray_iter):
        neighbor_indices = []
        center = []

        # Create indices for variable numbers of ndarray dimensions
        # to define a slice for the neighboring ndarray and the
        # center of the ndarray
        for idx, element in enumerate(prod):
            min_dim = max(0, element - 1)
            max_dim = min(ndarray.shape[idx], element + 2)
            neighbor_indices.append(slice(min_dim, max_dim))
            center.append(element)

        neighbor_indices = tuple(neighbor_indices)
        center = tuple(center)

        neighbor_ndarray = ndarray[neighbor_indices]
        active_count = neighbor_ndarray.sum()

        # Remove self from the sum
        active_count -= ndarray[center]

        # Determine the new value for the element based on the
        # state of the element and it's neighbors
        new_ndarray[center] = ndarray[center]
        if ndarray[center]:
            if active_count not in [2, 3]:
                new_ndarray[center] = 0
        elif active_count == 3:
            new_ndarray[center] = 1

    return new_ndarray


def pad_ndarray(ndarray):
    """
    Extend the ndarray by padding zero's adjecent to the edges/planes
    of the ndarray.

    This is needed between processing phases to expand the ndarray as the
    the pattern grows.
    """
    ndimensions = len(ndarray.shape)

    pad_width = tuple([(1, 1)] * ndimensions)
    ndarray = np.pad(ndarray, pad_width, constant_values=0)
    return ndarray


@click.command()
@click.option('--filename', default='input.txt', help='file containing input')
@click.option('--dimensions', default=3,
              help='n-dimensional conway simulation')
@click.option('--iterations', default=6,
              help='Number of iterations to run')
def main(filename, dimensions, iterations):
    """
    Day 17: Conway Cubes
    """

    if dimensions < 2 or dimensions > 5:
        print('The number of dimentions must be between 2 and 5.')
        quit(1)

    input_array = read_file(filename)
    ndarray = create_ndarray(input_array, dimensions)

    for count in range(1, iterations + 1):
        ndarray = pad_ndarray(ndarray)
        ndarray = process_ndarray(ndarray)

    # print(f'{ndarray = }')
    print(int(ndarray.sum()))


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
