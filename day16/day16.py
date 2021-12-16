with open('input') as f:
    packet_hex = f.readline().strip('\n')

packet = ''
for char in packet_hex:
    packet += format(int(char, base=16), '0>4b')


def parse_packet(pointer):
    init_pointer = pointer
    version = int(packet[pointer:pointer+3], base=2)
    pointer += 3
    type_id = int(packet[pointer:pointer+3], base=2)
    pointer += 3
    sub_packets = []
    if type_id == 4:
        literal = ''
        while True:
            chunk = packet[pointer:pointer+5]
            literal += chunk[1:]
            pointer += 5
            if chunk[0] == '0':
                break
        packet_value = int(literal, base=2)
    else:
        length_type = packet[pointer]
        pointer += 1
        if length_type == '0':
            sub_packet_length = int(packet[pointer:pointer+15], base=2)
            pointer += 15
            total_sub_packet_size = 0
            while total_sub_packet_size < sub_packet_length:
                sub_packet = parse_packet(pointer)
                total_sub_packet_size += sub_packet['packet_size']
                pointer += sub_packet['packet_size']
                sub_packets.append(sub_packet)
        else:
            num_sub_packets = int(packet[pointer:pointer+11], base=2)
            pointer += 11
            while len(sub_packets) < num_sub_packets:
                sub_packet = parse_packet(pointer)
                pointer += sub_packet['packet_size']
                sub_packets.append(sub_packet)
        if type_id == 0:
            packet_value = sum(sub_packet['packet_value'] for sub_packet in sub_packets)
        elif type_id == 1:
            packet_value = 1
            for sub_packet in sub_packets:
                packet_value = packet_value * sub_packet['packet_value']
        elif type_id == 2:
            packet_value = float('inf')
            for sub_packet in sub_packets:
                packet_value = min(packet_value, sub_packet['packet_value'])
        elif type_id == 3:
            packet_value = 0
            for sub_packet in sub_packets:
                packet_value = max(packet_value, sub_packet['packet_value'])
        elif type_id == 5:
            packet_value = int(sub_packets[0]['packet_value'] > sub_packets[1]['packet_value'])
        elif type_id == 6:
            packet_value = int(sub_packets[0]['packet_value'] < sub_packets[1]['packet_value'])
        elif type_id == 7:
            packet_value = int(sub_packets[0]['packet_value'] == sub_packets[1]['packet_value'])
    packet_size = pointer - init_pointer
    return {
        'version': version,
        'type_id': type_id,
        'packet_value': packet_value,
        'sub_packets': sub_packets,
        'packet_size': packet_size,
    }

parsed_packet = parse_packet(0)

def sum_versions(packet):
     version = packet['version']
     for sub_packet in packet['sub_packets']:
         version += sum_versions(sub_packet)
     return version

print(sum_versions(parsed_packet))
print(parsed_packet['packet_value'])

