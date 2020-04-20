# SNMP2TELEGRAF

SNMP2TELEGRAF is used to create Telegraf SNMP Inputs from MIBs files



## Example 1

Create a Telegraf SNMP inputs for SNMPv2-MIB

```bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/SNMPv2-MIB 1.3.6.1.2.1.1
```

Then move it to the telegraf.d folder
```bash
sudo mv INPUTS_SNMPv2-MIB.conf /etc/telegraf/telegraf.d/
```

Restart Telegraf
```bash
sudo service telegraf restart
```

Check status
```bash
sudo service telegraf status
```

## Example 2

Create a Telegraf SNMP inputs for IF-MIB

```bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/IF-MIB 1.3.6.1.2.1.2
```

Then move it to the telegraf.d folder
```bash
sudo mv INPUTS_IF-MIB.conf /etc/telegraf/telegraf.d/
```


Restart Telegraf
```bash
sudo service telegraf restart
```

Check status
```bash
sudo service telegraf status
```