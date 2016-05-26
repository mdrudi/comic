# Sea Over Land Function, Paolo Oliveri, May 12 2016
# This function ONLY works with numpy.ma masked 2D arrays or ND arrays
# working with the last two axes (not working with NaNs or other)
# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
# np.set_printoptions(threshold=np.nan)  # It slows debugging


def seaoverland(input_matrix, nloop=1):  # depth is to select the number of consequential mask points to fill
    # depth loop
    for loop in range(nloop):
        if np.sum(input_matrix.mask) == 0:  # nothing to fill
            return input_matrix
        else:
            # Create a nD x 8 3D matrix in which, last dimension fixed, the other dimensions
            #  contains values that are shifted in one of the 8 possible directions
            # of the last two axes compared to the original matrix
            shift_matrix = ma.array(np.empty(shape=(input_matrix.shape + (8,))),
                                    mask=False, fill_value=1.e20, dtype=float)
            # up shift
            shift_matrix[..., : - 1, :, 0] = input_matrix[..., 1:, :]
            # down shift
            shift_matrix[..., 1:, :, 1] = input_matrix[..., 0: - 1, :]
            # left shift
            shift_matrix[..., :, : - 1, 2] = input_matrix[..., :, 1:]
            # right shift
            shift_matrix[..., :, 1:, 3] = input_matrix[..., :, : - 1]
            # up-left shift
            shift_matrix[..., : - 1, : - 1, 4] = input_matrix[..., 1:, 1:]
            # up-right shift
            shift_matrix[..., : - 1, 1:, 5] = input_matrix[..., 1:, : - 1]
            # down-left shift
            shift_matrix[..., 1:, : - 1, 6] = input_matrix[..., : - 1, 1:]
            # down-right shift
            shift_matrix[..., 1:, 1:, 7] = input_matrix[..., : - 1, : - 1]
            # Mediate the shift matrix among the third dimension
            mean_matrix = ma.mean(shift_matrix, -1)
            # Replace input masked points with new ones belonging to the mean matrix
            output_matrix = ma.array(np.where(mean_matrix.mask + input_matrix.mask, mean_matrix, input_matrix),
                                     mask=mean_matrix.mask, fill_value=1.e20, dtype=float)
            output_matrix = ma.masked_where(mean_matrix.mask, output_matrix)
    return output_matrix
