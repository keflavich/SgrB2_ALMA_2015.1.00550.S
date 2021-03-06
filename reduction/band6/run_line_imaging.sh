#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.

WORK_DIR='/lustre/aginsbur/sgrb2/2016.1.00550.S/calibrated'
WORK_DIR='/lustre/aginsbur/sgrb2/2016.1.00550.S/science_goal.uid___A001_X879_X160/group.uid___A001_X879_X161/member.uid___A001_X879_X162/calibrated'
cd ${WORK_DIR}
REDUCTION_DIR='/lustre/aginsbur/sgrb2/2016.1.00550.S/reduction'

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa --nogui --nologger -c "execfile('$REDUCTION_DIR/scriptForImaging_lines.py')"

#export CASAPATH=/home/casa/packages/RHEL6/release/casa-release-5.1.0-74
#export PATH=${CASAPATH}/bin:$PATH
#
#export CASACMD="execfile('$REDUCTION_DIR/scriptForImaging_lines.py')"
#echo $CASACMD
#
#mpicasa -machinefile $PBS_NODEFILE casa -quiet --nogui --nologger --log2term -c "${CASACMD}"
