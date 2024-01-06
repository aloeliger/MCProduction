import argparse
import datetime
import subprocess
import os

parser = argparse.ArgumentParser(description='submit the gen-sim step for 2023 SUEP MC')
parser.add_argument(
    '--numEventsTotal',
    '-n',
    required=True,
    type=int,
    nargs='?',
    help='Total number of events to generate'
)
parser.add_argument(
    '--numEventsPerJob',
    '-j',
    required=True,
    type=int,
    nargs='?',
    help='Number of events per job'
)

args = parser.parse_args()

todaysDate = datetime.datetime.now().strftime('%d%b%Y_%H%M')

jobName = f'SUEP2023_{todaysDate}'

nfs_location = f'/nfs_scratch/aloeliger/MCGeneration/{jobName}/'
dag_location = f'{nfs_location}/dags/'
os.makedirs(dag_location, exist_ok=True)
submit_location = f'{nfs_location}/submit/'
output_dir = f'/store/user/aloeliger/MCGeneration/{jobName}/'
config = f'{os.environ["CMSSW_BASE"]}/src/MCProduction/SUEPProduction/python/SUEP_GEN_SIM_2023.py'

farmout_command = [
    'farmoutRandomSeedJobs',
    f"--submit-dir={submit_location}",
    f"--output-dir={output_dir}",
    # f"--output-dag-file={dag_location}/dag"
    # f"--opsys CentOS7",
    "--use-singularity CentOS7",
    "--memory-requirements 4000",
    f'{jobName}',
    str(args.numEventsTotal),
    str(args.numEventsPerJob),
    f'{os.environ["CMSSW_BASE"]}',
    config,
    "\'outputFile=$outputFileName\'",
    "\'nEventsPerJob=$nEventsPerJob\'",
    "\'randomSeed=$randomNumber\'",
]

farmout_command = ' '.join(farmout_command)

print('Farmout command:')
print(farmout_command)

finishedProcess = subprocess.run(
    [farmout_command],
    shell=True,
    check=True,
)