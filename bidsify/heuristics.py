import os
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    fmap_mag =  create_key('sub-{subject}/fmap/sub-{subject}_run-00{item:01d}_magnitude')
    fmap_phase = create_key('sub-{subject}/fmap/sub-{subject}_run-00{item:01d}_phasediff')
    func = create_key('sub-{subject}/func/sub-{subject}_task-machinegame_run-00{item:01d}_bold')
    func_sbref = create_key('sub-{subject}/func/sub-{subject}_task-machinegame_run-00{item:01d}_bold')
    info = {t1w: [], fmap_mag: [], fmap_phase: [], func: [], func_sbref: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim1 == 256) and (s.dim2 == 256) and ('T1w_MPR1_PMC' in s.protocol_name):
            info[t1w].append(s.series_id)
        if (s.dim3 == 112) and (s.dim4 == 1) and ('fieldmap' in s.protocol_name):
            info[fmap_mag].append(s.series_id)
        if (s.dim3 == 56) and (s.dim4 == 1) and ('fieldmap' in s.protocol_name):
            info[fmap_phase].append(s.series_id)
        if (s.dim3 == 56) and (s.dim4 == 1) and ('task001' in s.protocol_name):
            info[func].append(s.series_id)
        if (s.dim3 == 56) and (s.dim4 == 216) and ('task001' in s.protocol_name):
            info[func_sbref].append(s.series_id)
    return info
