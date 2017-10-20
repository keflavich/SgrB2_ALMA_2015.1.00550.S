from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata(dbservice=False, vis=['uid___A002_Xc44eb5_X1139', 'uid___A002_Xc483da_Xa88'], session=['session_1', 'session_2'])
    fixsyscaltimes(vis = 'uid___A002_Xc483da_Xa88.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_Xc44eb5_X1139.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hifa_importdata(dbservice=False, vis=['uid___A002_Xc44eb5_X1139', 'uid___A002_Xc483da_Xa88'], session=['session_1', 'session_2'])
    hifa_flagdata(pipelinemode="automatic")
    hifa_fluxcalflag(pipelinemode="automatic")
    hif_rawflagchans(pipelinemode="automatic")
    hif_refant(pipelinemode="automatic")
    hifa_tsyscal(pipelinemode="automatic")
    hifa_tsysflag(pipelinemode="automatic")
    hifa_antpos(pipelinemode="automatic")
    hifa_wvrgcalflag(pipelinemode="automatic")
    hif_lowgainflag(pipelinemode="automatic")
    hif_gainflag(pipelinemode="automatic")
    hif_setjy(pipelinemode="automatic")
    hifa_bandpass(pipelinemode="automatic")
    hifa_spwphaseup(pipelinemode="automatic")
    hifa_gfluxscale(pipelinemode="automatic")
    hifa_timegaincal(pipelinemode="automatic")
    hif_applycal(pipelinemode="automatic")
    hif_makeimlist(intent='PHASE,BANDPASS,CHECK')
    hif_makeimages(pipelinemode="automatic")
    hif_checkproductsize(maxproductsize=400.0, maxcubesize=30.0)
finally:
    h_save()
