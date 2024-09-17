# Copyright 2023 The GPU4PySCF Authors. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

############################################################
#  Example of DFT with PCM solvent model
############################################################

import numpy as np
import pyscf
from gpu4pyscf.dft import rks

atom ='''
O       0.0000000000    -0.0000000000     0.1174000000
H      -0.7570000000    -0.0000000000    -0.4696000000
H       0.7570000000     0.0000000000    -0.4696000000
'''

mol = pyscf.M(atom=atom, basis='def2-tzvpp')
mf = rks.RKS(mol, xc='HYB_GGA_XC_B3LYP').density_fit()
mf = mf.PCM()
mf.grids.atom_grid = (99,590)
mf.with_solvent.lebedev_order = 29 # 302 Lebedev grids
mf.with_solvent.method = 'IEF-PCM'
mf.with_solvent.eps = 78.3553
mf.kernel()

gradobj = mf.nuc_grad_method()
f = gradobj.kernel()

hessobj = mf.Hessian()
hess = hessobj.kernel()

# mass weighted hessian
mass = [15.99491, 1.00783, 1.00783]
for i in range(3):
    for j in range(3):
        hess[i,j] = hess[i,j]/np.sqrt(mass[i]*mass[j])


