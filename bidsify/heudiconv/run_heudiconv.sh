set -e
for subnum in 100057 311479 100003 100009 100042 100051 100059 100060 100063 100068 100103 100104 100105 100109 100110 100128 100129 100143 100152 100169 100180 100185 100188 100191 100207 100214 100215 100241 100243 100244 100247 100250 200025 200027 200056 200061 200081 200085 200088 200133 200148 200156 200162 200164 200166 200168 200173 200199 200211 200213 200249 304228 306065 306587 308023 310949 311047 311283 311444 311760 400285 400742 402997 405027 406925 406980 406989 407209 407672 408394 408511 408662 408952 408988 409381 409850 409874 411236 411256 411477
do
sed -e "s/{SUBNUM}/$subnum/g" run_heudiconv.batch | sbatch
done

module load dcm2niix/7July2016

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}*/scans/*/DICOM/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 100062 -c dcm2niix -b --overwrite

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}*/scans/*/DICOM/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 406620 -c dcm2niix -b --overwrite

heudiconv -d /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/*{subject}/scans/*/resources/DICOM/files/*.dcm -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/04_HEUDICONV_conversion/ -f /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/heudiconv/heuristics.py -s 407260 -c dcm2niix -b --overwrite
