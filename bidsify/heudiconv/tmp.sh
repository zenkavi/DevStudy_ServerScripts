set -e
for subnum in 200249 304228 306065 306587 308023 310949 311047 311283 311444 311760 400285 400742 402997 405027 406925 406980 406989 407209 407672 408394 408511 408662 408952 408988 409381 409850 409874 411236 411256 411477
do
sed -e "s/{SUBNUM}/$subnum/g" run_heudiconv.batch | sbatch
done

module load dcm2niix/7July2016

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}*/scans/*/DICOM/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 100062 -c dcm2niix -b --overwrite

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}*/scans/*/DICOM/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 406620 -c dcm2niix -b --overwrite

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}/scans/*/resources/DICOM/files/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 407260 -c dcm2niix -b --overwrite
