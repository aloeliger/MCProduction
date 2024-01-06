import argparse
import datetime
import subprocess
import os

parser = argparse.ArgumentParser(description='submit the RECO step for 2023 SUEP MC')
parser.add_argument(
    '--fileList',
    '-f',
    required=True,
    type=str,
    nargs='?',
    help='List of files to perform the reco step on'
)
parser.add_argument(
    '--nFilesPerJob',
    '-n',
    default=1,
    type=int,
    nargs='?',
    help='number of files for each job to process',
)

args = parser.parse_args()

todaysDate = datetime.datetime.now().strftime('%d%b%Y_%H%M')

jobName = f'SUEP2023_RECO_{todaysDate}'

nfs_location = f'/nfs_scratch/aloeliger/MCGeneration/{jobName}/'
dag_location = f'{nfs_location}/dags/'
os.makedirs(dag_location, exist_ok=True)
submit_location = f'{nfs_location}/submit/'
output_dir = f'/store/user/aloeliger/MCGeneration/{jobName}/'
config = f'{os.environ["CMSSW_BASE"]}/src/MCProduction/SUEPProduction/python/SUEP_RECO_2023.py'

farmout_command = [
    'farmoutAnalysisJobs',
    f"--submit-dir={submit_location}",
    f"--output-dir={output_dir}",
    f"--output-dag-file={dag_location}/dag",
    "--use-singularity CentOS7",
    "--memory-requirements 8000",
    f"--input-files-per-job={args.nFilesPerJob}",
    f"--input-file-list={args.fileList}",
    f'{jobName}',
    f'{os.environ["CMSSW_BASE"]}',
    config,
    "\'outputFile=$outputFileName\'",
    "\'inputFiles=$inputFileNames\'"
]

farmout_command = ' '.join(farmout_command)

print('Farmout command:')
print(farmout_command)

finishedProcess = subprocess.run(
    [farmout_command],
    shell=True,
    check=True,
)