#!/bin/sh

if [ -d "~/Programme/iec/IB-Peric/" ]; then
    echo "Not on Jonas work station"
    exit 0
fi

cd ~/Programme/iec/IB-Peric/source
python3 ~/Programme/iec/flint/src/flint.py check mod_*.f90 prog.f90 Grid/*.f90 Geometry/geom.f90 Geometry/mod_geometry.f90

exit $?
