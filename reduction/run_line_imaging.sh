#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.

WORK_DIR='/lustre/aginsbur/sgrb2/2016.1.00550.S/reduction'
cd ${WORK_DIR}

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$WORK_DIR/scriptForImaging_lines.py')"
#xvfb-run casapy --nogui -c "spwlist='0'; $SCRIPTPATH/fullcube_r0.py"
#xvfb-run casa --nogui -c "spwlist='0'; execfile('$SCRIPTPATH/fullcube_r0.py')"
