import os


def print_hardware_availability(check_gpu: bool = True, check_slurm: bool = True):
    """Print available CPU and GPU cores, memory, and other Slurm-related info"""
    res = {}

    # Check total number of CPU cores on the node
    num_cpu_cores_total = os.cpu_count()
    res["num_cpu_cores_total"] = num_cpu_cores_total
    print(f"Total CPU cores on the node: {num_cpu_cores_total}")

    # Check number of available CPU cores
    num_cpu_cores_available = len(os.sched_getaffinity(0))
    res["num_cpu_cores_available"] = num_cpu_cores_available
    print(f"Total CPU cores available: {num_cpu_cores_available}")

    if check_gpu:
        # Check visible CUDA devices
        cuda_visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
        if cuda_visible_devices is None or cuda_visible_devices == "":
            res["is_cuda_available"] = False
            print(f"CUDA not available")
        else:
            num_cuda_devices = len(cuda_visible_devices.split(","))
            res["num_cuda_devices"] = num_cuda_devices
            print(f"Number of available CUDA devices: {num_cuda_devices}")

        # Check accessibility of GPUs by torch
        try:
            import torch

            res["is_torch_available"] = True

            is_cuda_available = torch.cuda.is_available()
            res["is_cuda_available"] = is_cuda_available
            if is_cuda_available:
                gpu_names = [
                    torch.cuda.get_device_name(i)
                    for i in range(torch.cuda.device_count())
                ]
                res["gpu_names"] = gpu_names
                for i, name in enumerate(gpu_names):
                    print(f"  GPU {i}: {name}")
            else:
                res["gpu_names"] = "(pytorch unavailable)"
        except ImportError:
            res["is_torch_available"] = False
            print("Cannot import pytorch")

    # Check Slurm-related env vars
    if check_slurm:
        print("Slurm-related environment variables:")
        env_vars_to_check = [
            "SLURM_NODELIST",
            "SLURM_NTASKS",
            "SLURM_TASKS_PER_NODE",
            "SLURM_TRES_PER_TASK",
            "SLURM_MEM_PER_NODE",
        ]
        res["slurm_env_vars"] = {}
        for env_var in env_vars_to_check:
            val = os.getenv(env_var)
            if not val:
                val = "(unset)"
            elif env_var == "SLURM_MEM_PER_NODE" and val.isdigit():
                val = f"{int(val) / 1024}GB"
            print(f"  {env_var}={val}")
            res["slurm_env_vars"][env_var] = val

    return res


if __name__ == "__main__":
    print_hardware_availability(check_gpu=True, check_slurm=True)
