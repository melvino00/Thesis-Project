import docker
import csv
import time

client = docker.from_env()

target_services = ["api_gateway", "auth_service", "data_service", "user_service"]
active_containers = []

print("Searching for containers...")
for container in client.containers.list():
    for target in target_services:
        if target in container.name:
            active_containers.append(container)

if not active_containers:
    print("Couldn't find containers, ensure that 'docker compose up -d' is running?")
    exit()

container_names = [c.name for c in active_containers]
print(f"Recording started for: {container_names}")
print("Run k6-test now. Ctrl+C to end recording.")

with open('metrics_output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Container", "CPU_Perc"])
    
    print("Recording started. Running k6-test now...")
    try:
        while True:
            for c in active_containers:
                try:
                    stats = c.stats(stream=False)

                    cpu_stats = stats.get('cpu_stats', {})
                    precpu_stats = stats.get('precpu_stats', {})
                    
                    cpu_delta = cpu_stats.get('cpu_usage', {}).get('total_usage', 0) - precpu_stats.get('cpu_usage', {}).get('total_usage', 0)
                    sys_delta = cpu_stats.get('system_cpu_usage', 0) - precpu_stats.get('system_cpu_usage', 0)
                    
                    online_cpus = cpu_stats.get('online_cpus')
                    if not online_cpus:
                        percpu_usage = cpu_stats.get('cpu_usage', {}).get('percpu_usage')
                        online_cpus = len(percpu_usage) if percpu_usage else 1

                    if sys_delta > 0 and cpu_delta > 0:
                        cpu_perc = (cpu_delta / sys_delta) * online_cpus * 100.0
                    else:
                        cpu_perc = 0.0
                        
                    writer.writerow([time.time(), c.name, f"{cpu_perc:.2f}"]).replace('.', ',') # Replace dot with comma for decimal
                    
                except Exception as e:
                    print(f"Could not read stas for {c.name}. Error: {e}")
            
            time.sleep(1) # Sampling frequency 1 second
    except KeyboardInterrupt:
        print("Recording ended.")