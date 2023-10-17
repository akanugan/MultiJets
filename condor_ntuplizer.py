#!/usr/bin/env python

import os
import subprocess
import shutil
print(os.environ['PATH'])

def submit_condor_jobs(input_file, nfPerJob, isdata=0):
    condor_submit_path = "/usr/local/bin/condor_submit"
    # Set the required information for Condor job submission
    exe_script = "worker2.sh"
    exe_ana = "make_flat_jettuple_ak4.py"
    dataset_ana = "MC_2016"
    files_to_transfer = f"{input_file},{exe_ana}"
    base_output_directory = "/uscms/home/akanugan/nobackup/MultiJets/condor_out"

 
    with open(input_file, 'r') as file:
        lines = file.readlines()
    fname = [line.strip() for line in lines]

    # Split the input files into smaller lists for each job
    jobid = 0
    for i in range(0, len(fname), nfPerJob):
        output_filename = f"FileList_{input_file[:-4]}_job{jobid}.txt"  
        with open(output_filename, 'w') as outf:
            for j in range(nfPerJob):
                if i + j < len(fname):
                    outf.write(fname[i + j] + "\n")
        job_name = f"{input_file[:-4]}_job{jobid}"  # Unique job name
        jobid += 1

        # Create Condor job submission file for each job
        with open(f"{job_name}.submit", 'w') as submit_file:
            submit_file.write("universe = vanilla\n")
            submit_file.write(f"Executable = {exe_script}\n")
            submit_file.write("Should_Transfer_Files = YES\n")
            submit_file.write("WhenToTransferOutput = ON_EXIT_OR_EVICT\n")
            submit_file.write(f"Transfer_Input_Files = {files_to_transfer},{output_filename}\n")
            submit_file.write(f"Output = {job_name}.stdout\n")
            submit_file.write(f"Error = {job_name}.stderr\n")
            submit_file.write(f"Log = {job_name}.condor\n")
            submit_file.write(f"Arguments = {exe_ana} {output_filename} {isdata}\n")
            submit_file.write("+LENGTH=\"SHORT\"\n\n")
            submit_file.write("queue 1")

            #Submit each Condor job
            #subprocess.Popen(["condor_submit", f"{job_name}.submit"])
        os.system(f"{condor_submit_path} {job_name}.submit")       
        

if __name__ == "__main__":
    submit_condor_jobs("QCD_test.txt", 1, isdata=0)
