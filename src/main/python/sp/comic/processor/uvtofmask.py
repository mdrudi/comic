# Umask, Vmask to Fmask Function, Paolo Oliveri, Jul 22 2016
# This function ONLY works with numpy.ma masked ND arrays with N >=3,
# working with the last two axes (not working with NaNs or other)
# -*- coding: utf-8 -*-
import numpy as np
# np.set_printoptions(threshold=np.nan)  # It slows debugging


def uvtofmask(umask, vmask):
    if umask.shape == vmask.shape:
        fumask = np.zeros(shape=umask.shape, dtype=int)
        fvmask = np.zeros(shape=vmask.shape, dtype=int)
        umask = 1 * np.invert(umask)
        vmask = 1 * np.invert(vmask)
        fumask[..., : - 1, :] = umask[..., : - 1, :] * umask[..., 1:, :]
        fvmask[..., :, : - 1] = vmask[..., :, : - 1] * vmask[..., :, 1:]
        fmask = fumask + fvmask
        fmask = np.invert(fmask.astype(bool))
    else:
        raise ValueError('umask and vmask have not the same size.')
    return fmask
