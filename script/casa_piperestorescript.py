from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata (dbservice=False, bdfflags=False, vis=['../rawdata/uid___A002_Xc44eb5_X1139', '../rawdata/uid___A002_Xc483da_Xa88'], session=['session_1', 'session_2'], ocorr_mode='ca')
    fixsyscaltimes(vis = 'uid___A002_Xc483da_Xa88.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_Xc44eb5_X1139.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hif_restoredata (vis=['uid___A002_Xc44eb5_X1139', 'uid___A002_Xc483da_Xa88'], session=['session_1', 'session_2'], ocorr_mode='ca')
finally:
    h_save()
