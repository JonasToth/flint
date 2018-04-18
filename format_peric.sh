#!/bin/sh

if [ ! -d ~/Programme/iec/IB-Peric/ ] || [ ! -d ~/Programme/iec/flint/ ]; then
    echo "Not on Jonas work station"
    exit 0
fi

cd ~/Programme/iec/IB-Peric/source

# git stash
fprettify -i 2 -w 2 mod_*.f90 prog.f90 Grid/*.f90 Geometry/mod_geometry.f90
python3 ~/Programme/iec/flint/src/flint.py format mod_*.f90 prog.f90 Grid/*.f90 Geometry/mod_geometry.f90
STATUS=$?

# git checkout -- mod_*.f90 prof.f90 Grid/*.f90 Geometry/geom.f90 Geometry/mod_geometry.f90
# git stash apply

echo "Restore with:"
echo "$ git checkout -- mod_kinds.f90 mod_constants.f90 mod_solver.f90 mod_utility.f90 prog.f90 Grid/mod_multigrid.f90 Geometry/geom.f90 Geometry/mod_geometry.f90"
# echo "$ git stash apply"

exit $STATUS
