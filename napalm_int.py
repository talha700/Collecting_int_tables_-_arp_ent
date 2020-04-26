from napalm import get_network_driver
import json
import yaml

with open("my_inventory.yml") as f:
        data = yaml.safe_load(f)


for k,v in data["Devices"].items():
    if k != "CSR1000v":
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

