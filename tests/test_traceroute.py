

import socket
import struct
import time
import requests


class Traceroute:
   
    
    def __init__(self, destination, max_hops=30, timeout=2, num_probes=3):
       
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        self.num_probes = num_probes
        self.dest_ip = None
        self.results = []
    
    def resolve_hostname(self):
        
        try:
            self.dest_ip = socket.gethostbyname(self.destination)
            return True
        except socket.gaierror:
            return False
    
    def calculate_checksum(self, data):
        
        checksum = 0
        count_to = (len(data) // 2) * 2
        
        for count in range(0, count_to, 2):
            val = data[count + 1] * 256 + data[count]
            checksum += val
            checksum &= 0xffffffff
        
        if count_to < len(data):
            checksum += data[len(data) - 1]
            checksum &= 0xffffffff
        
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16
        answer = ~checksum & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        
        return answer
    
    def create_icmp_packet(self, packet_id, sequence):
        
        icmp_type = 8  
        icmp_code = 0
        checksum = 0
        
        
        header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, 
                           packet_id, sequence)
        
       
        data = b'traceroute_data'
        
        
        checksum = self.calculate_checksum(header + data)
        
       
        header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, 
                           packet_id, sequence)
        
        return header + data
    
    def send_probe(self, ttl, packet_id, sequence):
        
        try:
            
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                       socket.IPPROTO_ICMP)
            send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                       socket.IPPROTO_ICMP)
            recv_socket.settimeout(self.timeout)
            
            
            packet = self.create_icmp_packet(packet_id, sequence)
            send_time = time.time()
            send_socket.sendto(packet, (self.dest_ip, 1))
            
            
            try:
                data, addr = recv_socket.recvfrom(1024)
                recv_time = time.time()
                rtt = (recv_time - send_time) * 1000  
                router_ip = addr[0]
                
                send_socket.close()
                recv_socket.close()
                return router_ip, rtt
                
            except socket.timeout:
                send_socket.close()
                recv_socket.close()
                return None, None
                
        except PermissionError:
            return "PERMISSION_ERROR", None
        except Exception as e:
            return None, None
    
    def get_hostname(self, ip):
        
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return ip
    
    def get_geolocation(self, ip):
       
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'isp': data.get('isp', 'Unknown')
                    }
        except:
            pass
        return None
    
    def trace(self, with_geo=False):
       
        if not self.resolve_hostname():
            return {
                'success': False,
                'error': f'Cannot resolve hostname: {self.destination}'
            }
        
        packet_id = 12345
        reached = False
        
       
        for ttl in range(1, self.max_hops + 1):
            hop_data = {
                'ttl': ttl,
                'probes': []
            }
            
            router_ips = []
            rtts = []
            
            
            for probe in range(self.num_probes):
                router_ip, rtt = self.send_probe(ttl, packet_id, probe)
                
                if router_ip == "PERMISSION_ERROR":
                    return {
                        'success': False,
                        'error': 'Permission denied. Run as administrator/root.'
                    }
                
                hop_data['probes'].append({
                    'ip': router_ip,
                    'rtt': rtt
                })
                
                if router_ip:
                    router_ips.append(router_ip)
                    rtts.append(rtt)
                
                packet_id += 1
            
            
            if router_ips:
                primary_ip = router_ips[0]
                hostname = self.get_hostname(primary_ip)
                avg_rtt = sum(rtts) / len(rtts) if rtts else None
                
                hop_data['ip'] = primary_ip
                hop_data['hostname'] = hostname
                hop_data['avg_rtt'] = round(avg_rtt, 2) if avg_rtt else None
                hop_data['all_rtts'] = [round(r, 2) if r else None for r in rtts]
                
              
                if with_geo:
                    geo = self.get_geolocation(primary_ip)
                    hop_data['location'] = geo
                
              
                if primary_ip == self.dest_ip:
                    reached = True
                    hop_data['is_destination'] = True
                    self.results.append(hop_data)
                    break
            else:
                hop_data['ip'] = None
                hop_data['hostname'] = 'Timeout'
                hop_data['avg_rtt'] = None
                hop_data['all_rtts'] = [None, None, None]
            
            self.results.append(hop_data)
        
        return {
            'success': True,
            'destination': self.destination,
            'dest_ip': self.dest_ip,
            'reached': reached,
            'total_hops': len(self.results),
            'hops': self.results
        }


def simple_traceroute(destination, max_hops=30):
    
    tracer = Traceroute(destination, max_hops=max_hops)
    return tracer.trace(with_geo=True)