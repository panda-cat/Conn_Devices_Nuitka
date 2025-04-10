"""
lldpwin.py - Windows LLDP/CDP嗅探工具
需要管理员权限运行
安装依赖: pip install scapy
"""
import argparse
import ctypes
import sys
from scapy.all import *
from scapy.contrib.lldp import LLDPDU
from scapy.contrib.cdp import CDPMsg

# 加载WinDivert驱动
try:
    windivert = ctypes.WinDLL("WinDivert.dll")
except FileNotFoundError:
    print("错误：需要将WinDivert.dll与程序放在同一目录")
    sys.exit(1)

def list_interfaces():
    """WinDivert不需要物理接口选择"""
    print("警告：WinDivert模式下接口选择无效")

def parse_management_address(tlv):
    """解析LLDP管理地址TLV (类型8)"""
    if len(tlv.value) < 5:
        return None
    
    addr_subtype = tlv.value[0]
    addr_length = tlv.value[1]
    addr_bytes = tlv.value[4:4+addr_length]
    
    try:
        if addr_subtype == 1:  # IPv4
            return ".".join(map(str, addr_bytes[:4]))
        elif addr_subtype == 2:  # IPv6
            return ":".join(f"{x:02x}" for x in addr_bytes)
    except IndexError:
        return None
    return None

def process_packet(pkt):
    """处理捕获的数据包"""
    ips = []  # 初始化IP列表
    
    if pkt.haslayer(LLDPDU):
        print("\n[LLDP设备发现]")
        print(f"接口: {pkt.sniffed_on}")
        print(f"源MAC: {pkt.src}")
        
        for layer in pkt[LLDPDU].tlvs:
            try:
                if layer.type == 1:
                    print(f"系统名称: {layer.value.decode('utf-8', errors='ignore')}")
                elif layer.type == 2:
                    print(f"端口描述: {layer.value.decode('utf-8', errors='ignore')}")
                elif layer.type == 3:
                    print(f"设备功能: {int.from_bytes(layer.value, 'big'):032b}")
                elif layer.type == 8:  # 管理地址
                    ip = parse_management_address(layer)
                    if ip:
                        ips.append(f"管理IP: {ip}")
            except Exception as e:
                print(f"解析错误: {str(e)}")

    elif pkt.haslayer(CDPMsg):  # 更新检查CDP层的方法
        print("\n[CDP设备发现]")
        print(f"接口: {pkt.sniffed_on}")

        for cdp in pkt[CDPMsg].data:
            try:
                if cdp.type == 0x01:
                    print(f"设备名称: {cdp.value.decode('utf-8', errors='ignore')}")
                elif cdp.type == 0x02:  # 地址列表
                    addr_data = bytes(cdp.value)
                    if len(addr_data) >= 8:
                        num_ips = int.from_bytes(addr_data[4:8], 'big')
                        pos = 8
                        for _ in range(num_ips):
                            if pos + 8 > len(addr_data):
                                break
                            proto_type = int.from_bytes(addr_data[pos:pos+4], 'big')
                            pos += 4
                            addr_len = int.from_bytes(addr_data[pos:pos+4], 'big')
                            pos += 4
                            if pos + addr_len > len(addr_data):
                                break
                            if proto_type == 0x01:  # IPv4
                                ips.append("IPv4地址: " + ".".join(map(str, addr_data[pos:pos+4])))
                            pos += addr_len
            except Exception as e:
                print(f"CDP解析错误: {str(e)}")

    if ips:
        print("网络地址:")
        for ip in ips:
            print(f"  {ip}")

def main():
    # 强制使用WinDivert
    conf.use_win_divert = True
    
    parser = argparse.ArgumentParser()
    parser.add_argument('run', nargs='?', help='启动嗅探')
    parser.add_argument('-i', '--interface', help='此参数仅用于兼容')
    args = parser.parse_args()

    # 固定过滤规则
    filter_str = "ether dst 01:80:c2:00:00:0e or ether dst 01:00:0c:cc:cc:cc"
    
    try:
        sniff(filter=filter_str,
              prn=process_packet,
              store=0,
              timeout=30)
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
