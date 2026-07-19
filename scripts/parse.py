import pyshark
import math
from pprint import pprint

cap = pyshark.FileCapture(input_file='sf19us-MTA-lab-01.pcap', display_filter='dns.flags.response == 0')

packet_info = []
for packet in cap:
  try:
    data = {
      'timestamp': packet.sniff_time,
      'source_ip': packet.ip.src,
      'dns_location': packet.dns.qry_name,
    }
    packet_info.append(data)
  except AttributeError as error:
    pass

pprint(packet_info)


