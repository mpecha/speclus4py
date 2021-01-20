from petsc4py import PETSc

import numpy as np
import vtk

from speclus4py.tools.viewer import vis_result_2phase


def hdist_2phase_vol_img(file_img: str, labels: np.ndarray, verbose=False, visualize_result=False) -> int:
    vtk_reader = vtk.vtkXMLImageDataReader()
    vtk_reader.SetFileName(file_img)
    vtk_reader.Update()
    image_data = vtk_reader.GetOutput()

    dims = image_data.GetDimensions()
    N = (dims[0] - 1) * (dims[1] - 1) * (dims[2] - 1)

    # determine label of solid
    solid_label = 0
    image_scalars = image_data.GetCellData().GetScalars()
    for i in range(N):
        c = image_scalars.GetTuple1(i)
        if c == 255.:
            solid_label = labels[i]
            break

    hdist = 0
    for i in range(N):
        c = image_scalars.GetTuple1(i)
        if c == 255 and labels[i] != solid_label:
            hdist += 1
        elif c == 0 and labels[i] == solid_label:
            hdist += 1

    if verbose:
        PETSc.Sys.Print('Hamming distance: %d' % hdist)

    if visualize_result:
        vis_result_2phase(image_data, labels)

    return hdist