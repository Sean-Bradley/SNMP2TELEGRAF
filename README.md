# SNMP2TELEGRAF

SNMP2TELEGRAF is used to create Telegraf SNMP Inputs from MIBs files



## Example 1

Create a 
```bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/SNMPv2-MIB 1.3.6.1.2.1.1
```

Then move it to the telegraf.d folder
```bash
sudo mv INPUTS_SNMPv2-MIB.conf /etc/telegraf/telegraf.d/
```
