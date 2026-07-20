import pyshark
import math
from pprint import pprint
from collections import defaultdict

# load packets
cap = pyshark.FileCapture(input_file='pcap_files/sf19us-MTA-lab-01.pcap', display_filter='dns.flags.response == 0')

packets = []
for packet in cap:
  try:
    data = {
      'timestamp': packet.sniff_time,
      'source_ip': packet.ip.src,
      'dns_location': packet.dns.qry_name,
    }
    packets.append(data)
  except AttributeError as error:
    pass

# group by source ip and domain -> calculate coefficient of variance
grouped_packets = defaultdict(list)
for packet in packets:
  ip, dns = packet['source_ip'], packet['dns_location']
  grouped_packets[(ip, dns)].append(packet)

timing_scores = {}
for key, packets in grouped_packets.items():
  if len(packets) < 4:
    continue

  times = sorted(p['timestamp'] for p in packets)
  gaps = []
  for i in range(len(times)-1):
    gap = (times[i+1] - times[i]).total_seconds()
    gaps.append(gap)
  
  mean = sum(gaps) / len(gaps)
  if mean == 0:
    continue

  variance = sum((g - mean) ** 2 for g in gaps) / len(gaps)
  cv = (variance ** 0.5) / mean
  timing_scores[key] = cv




