"""
Traceroute Core Logic
Windows / WSL compatible version
"""

import subprocess
import platform
import re

def simple_traceroute(destination, max_hops=30):
    """
    System traceroute/tracert command ব্যবহার করে realistic results return করে
    """
    result = {
        'success': True,
        'destination': destination,
        'dest_ip': None,
        'reached': False,
        'total_hops': 0,
        'hops': []
    }

    try:
        system = platform.system()
        if system == "Windows":
            cmd = ["tracert", "-d", "-h", str(max_hops), destination]  # -d : skip hostnames, -h : max hops
        else:
            cmd = ["traceroute", "-n", "-m", str(max_hops), destination]  # Linux/Mac

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        lines = proc.stdout.splitlines()

        # Windows tracert output এ first line skip
        start_idx = 0
        if system == "Windows":
            while start_idx < len(lines) and not re.match(r'\s*1\s+', lines[start_idx]):
                start_idx += 1

        for line in lines[start_idx:]:
            line = line.strip()
            if not line:
                continue

            # Regex দিয়ে hop parse
            if system == "Windows":
                match = re.match(r"(\d+)\s+([\d*]+)\s+ms\s+([\d*]+)\s+ms\s+([\d*]+)\s+ms\s+([\d\.]+)?", line)
                if not match:
                    continue
                ttl = int(match.group(1))
                rtts = [float(match.group(i)) if match.group(i) != '*' else None for i in range(2,5)]
                ip = match.group(5) if match.group(5) else None
                hostname = ip if ip else "Timeout"
            else:
                # Linux traceroute output: ttl ip rtt1 rtt2 rtt3 ...
                parts = re.split(r'\s+', line)
                if len(parts) < 2:
                    continue
                try:
                    ttl = int(parts[0])
                except:
                    continue
                ip = parts[1] if parts[1] != "*" else None
                hostname = ip if ip else "Timeout"
                rtts = []
                for val in parts[2:]:
                    if "ms" in val:
                        try:
                            rtts.append(float(val.replace("ms","").strip()))
                        except:
                            rtts.append(None)
                    else:
                        rtts.append(None)
                rtts = rtts[:3]

            avg_rtt = round(sum([r for r in rtts if r is not None])/len([r for r in rtts if r is not None]),2) if any(rtts) else None

            hop = {
                'ttl': ttl,
                'probes': [{'ip': ip, 'rtt': r} for r in rtts[:3]],
                'ip': ip,
                'hostname': hostname,
                'avg_rtt': avg_rtt,
                'all_rtts': rtts[:3]
            }

            result['hops'].append(hop)

            if ip == destination:
                result['reached'] = True
                break

        result['total_hops'] = len(result['hops'])
        result['dest_ip'] = result['hops'][-1]['ip'] if result['hops'] else None

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
