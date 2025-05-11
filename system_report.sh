#!/bin/bash

timestamp=$(date +%F_%H-%M-%S)
log_dir="./logs"
log_file="$log_dir/report_$timestamp.log"

mkdir -p "$log_dir"

# CPU and Memory Usage
echo "===== CPU and Memory Usage =====" >> "$log_file"
top -b -n1 | head -n 5 >> "$log_file"
echo >> "$log_file"

# Top 5 CPU-consuming Processes
echo "===== Top 5 CPU-consuming Processes =====" >> "$log_file"
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6 >> "$log_file"
echo >> "$log_file"

# Disk usage
echo "===== Disk Usage (/ /var /home) =====" >> "$log_file"
df -h / /var /home >> "$log_file"
echo >> "$log_file"

# Network interfaces and IPs
echo "===== Network Interfaces and IPs =====" >> "$log_file"
ip -brief addr >> "$log_file"
echo >> "$log_file"

# Delete old logs (>14 days)
find "$log_dir" -name "*.log" -type f -mtime +14 -exec rm {} \;

echo "✅ Report saved at $log_file"

