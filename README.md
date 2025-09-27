# Slurm cheatsheet

```shell
# Submit job
sbatch $job_script_path

# Cancel job
scancel $jobid

# Check status of queued, pending, and running jobs
Squeue

# Interactive job on Kuma (GPU)
Sinteract -p l40s -q debug -t 1:00:00 -m 32G -c 8 -g gpu:1
Sinteract -p h100 -q debug -t 1:00:00 -m 64G -c 16 -g gpu:1

# Interactive job on Jed (CPU)
Sinteract -p standard -q serial -t 1:00:00 -m 64G -c 32

# Check priorities of queued jobs
sprio -S '-Y'
sprio -S '-Y' -l  # with extra info

# Check job details
scontrol show job $jobid

# Check usage
sausage
sausage --account upramdya  # check usage of the whole account

# Attach shell to existing job
# (when you're done, you can safely close the shell with ctrl+d without
# interrupting the job that it is attached to)
srun --pty --overlap --jobid $jobid bash
```
