import os

def save_randomise(randomise_results, in_path, mnum, reg):

    if len(randomise_results.outputs.tstat_files)>0:
        for i in range(0,len(randomise_results.outputs.tstat_files)):
            if tfce:
                os.rename(randomise_results.outputs.tstat_files[i], "%s/rand/rand_%s_%s_tstat%s_tfce.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.tstat_files[i], "%s/rand/rand_%s_%s_tstat%s_cluster.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved tstat_file for: %s %s"%(mnum, reg))
            print("***********************************************")

    if len(randomise_results.outputs.fstat_files)>0:
        for i in range(0,len(randomise_results.outputs.fstat_files)):
            if tfce:
                os.rename(randomise_results.outputs.fstat_files[i],"%s/rand/rand_%s_%s_fstat%s_tfce.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.fstat_files[i],"%s/rand/rand_%s_%s_fstat%s_cluster.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved fstat_file for: %s %s"%(mnum, reg))
            print("***********************************************")

    if len(randomise_results.outputs.t_p_files)>0:
        for i in range(0,len(randomise_results.outputs.t_p_files)):
            if tfce:
                os.rename(randomise_results.outputs.t_p_files[i], "%s/rand/rand_%s_%s_t_p%s_tfce.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.t_p_files[i], "%s/rand/rand_%s_%s_t_p%s_cluster.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved t_p_file for: %s %s"%(mnum, reg))
            print("***********************************************")

    if len(randomise_results.outputs.f_p_files)>0:
        for i in range(0,len(randomise_results.outputs.f_p_files)):
            if tfce:
                os.rename(randomise_results.outputs.f_p_files[i],"%s/rand/rand_%s_%s_f_p%s_tfce.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.f_p_files[i],"%s/rand/rand_%s_%s_f_p%s_cluster.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved f_p_file for: %s %s"%(mnum, reg))
            print("***********************************************")

    if len(randomise_results.outputs.t_corrected_p_files)>0:
        for i in range(0,len(randomise_results.outputs.t_corrected_p_files)):
            if tfce:
                os.rename(randomise_results.outputs.t_corrected_p_files[i],"%s/rand/rand_%s_%s_tfce_corrp_tstat%s.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.t_corrected_p_files[i],"%s/rand/rand_%s_%s_cluster_corrp_tstat%s.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved t_corrected_p_file for: %s %s"%(mnum, reg))
            print("***********************************************")

    if len(randomise_results.outputs.f_corrected_p_files)>0:
        for i in range(0,len(randomise_results.outputs.f_corrected_p_files)):
            if tfce:
                os.rename(randomise_results.outputs.f_corrected_p_files[i],"%s/rand/rand_%s_%s_tfce_corrp_fstat%s.nii.gz"%(in_path,mnum, reg, str(i+1)))
            else:
                os.rename(randomise_results.outputs.f_corrected_p_files[i],"%s/rand/rand_%s_%s_cluster_corrp_fstat%s.nii.gz"%(in_path,mnum, reg, str(i+1)))
            print("***********************************************")
            print("Saved t_corrected_p_file for: %s %s"%(mnum, reg))
            print("***********************************************")
