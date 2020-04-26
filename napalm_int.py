from napalm import get_network_driver
import yaml
from concurrent.futures import ThreadPoolExecutor


with open("my_inventory.yml") as f:
        data = yaml.safe_load(f)

all_devices = []
for k,v in data["Devices"].items():
   all_devices.append({k:v})

def main(devices):
    for k,v in devices.items():
        try:
            driver = get_network_driver(v["type"])

            device = driver(hostname = v["hostname"],
                            username = v["username"],
                            password = v["password"])
            device.open()
            data_1 =  device.get_arp_table()
            output_1 = yaml.dump({k : data_1} , indent=4)

            data_2 =  device.get_interfaces_counters()
            output_2 = yaml.dump({k : data_2} , indent=4)

            
            with open("arp_table.yaml","a") as w:
                    w.write(output_1)

            with open("int_counter.yaml","a") as f:
                    f.write(output_2)

            print(f'Success for {k}')
            
        except:
            print(f'Failed for {k}')


if __name__ == "__main__":
    with ThreadPoolExecutor() as t:
        exe = t.map(main,all_devices)
