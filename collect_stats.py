import docker
import csv
import time

client = docker.from_env()
containers = ["api_gateway", "auth_service", "data_service", "user_service"]

with open('metrics_output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Container", "CPU_Perc"])
    
    print("Recording started. Running k6-test now...")
    try:
        while True:
            for name in containers:
                try:
                    c = client.containers.get(name)
                    stats = c.stats(stream=False)

                    # Analyzes CPU % by Dockers standard formula
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                    sys_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                    if sys_delta > 0:
                        cpu_perc = (cpu_delta / sys_delta) * len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [1])) * 100.0
                        writer.writerow([time.time(), name, f"{cpu_perc:.2f}"])
                except: continue
            time.sleep(1) # Sampling frequency
    except KeyboardInterrupt:
        print("Recording ended.")