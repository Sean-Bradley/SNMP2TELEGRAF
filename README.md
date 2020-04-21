# SNMP2TELEGRAF

SNMP2TELEGRAF is used to create Telegraf SNMP Inputs from MIBs files


Usage: python SNMP2TELEGRAF.py Path-to-MIB-file Base-OID

python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/SNMPv2-MIB 1.3.6.1.2.1.1

eg,

## Ubuntu 18

```bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/SNMPv2-MIB 1.3.6.1.2.1.1
```

## Centos 7

```bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/SNMPv2-MIB 1.3.6.1.2.1.1
```

Then move the generated conf file to the telegraf.d folder
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


## Requirements

The server that you will use to create the templates will need to have several SNMP configurations and tools pre installed, plus the MIB files that you want to convert, plus any dependencies they require, and they will need to be correctly placed within the file system.

The **SNMP2TELEGRAF.py** script is also written in Python 2.7

## Install required SNMP dependencies

### Ubuntu 18

``` bash
sudo apt update
sudo apt install snmp snmp-mibs-downloader libsnmp-perl libsnmp-dev 
```

### Centos 7 

``` bash
yum check-update
yum install net-snmp-utils net-snmp-libs net-snmp-perl
```

Test **mib2c** works

``` bash
mib2c -h
```

Output should resemble this below with no errors displayed.

``` bash
/usr/bin/mib2c [-h] [-c configfile] [-f prefix] mibNode

  -h            This message.

  -c configfile Specifies the configuration file to use
                that dictates what the output of mib2c will look like.

  -I PATH       Specifies a path to look for configuration files in

  -f prefix     Specifies the output prefix to use.  All code
                will be put into prefix.c and prefix.h

  -d            debugging output (don't do it.  trust me.)

  -S VAR=VAL    Set $VAR variable to $VAL

  -i            Don't run indent on the resulting code

  -s            Don't look for mibNode.sed and run sed on the resulting code

  mibNode       The name of the top level mib node you want to
                generate code for.  By default, the code will be stored in
                mibNode.c and mibNode.h (use the -f flag to change this)
```

Try python

``` bash
python -V
```

If it doesn't say python 2.7.# then install python

### Ubuntu 18

``` bash
apt install python
```

### Centos 7

``` bash
yum install python
```

Now download the **SNMP2TELEGRAF.py** tool


``` bash
curl https://raw.githubusercontent.com/Sean-Bradley/SNMP2TELEGRAF/master/SNMP2TELEGRAF.py --output SNMP2TELEGRAF.py
```

Now are ready to continue.

## Example 1

Create Telegraf SNMP inputs for SNMPv2-MIB

### Ubuntu 18

``` bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/SNMPv2-MIB 1.3.6.1.2.1.1
```

### Centos 7

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/SNMPv2-MIB.txt 1.3.6.1.2.1.1
```


A new file called **INPUTS_SNMPv2-MIB.conf** should have been created.

Move the generated conf file to the telegraf.d folder, test it is ok and then restart the telegraf service.


## Example 2

Create Telegraf SNMP inputs for IF-MIB

### Ubuntu 18

``` bash
python SNMP2TELEGRAF.py /var/lib/snmp/mibs/ietf/IF-MIB 1.3.6.1.2.1.2
```

### Centos 7

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/IF-MIB.txt 1.3.6.1.2.1.2
```

A new file called **INPUTS_IF-MIB.conf** should have been created.

Move the generated conf file to the telegraf.d folder, test it is ok and then restart the telegraf service.


## Example 3

This is slightly more complicated.
First we need to download a generic Huawei MIB file.

``` bash
curl http://www.circitor.fr/Mibs/Mib/H/HUAWEI-MIB.mib > HUAWEI-MIB.mib
```

Now to create the SNMP inputs for the generic Huawei device

``` bash
python SNMP2TELEGRAF.py ./HUAWEI-MIB.mib 1.3.6.1
```

A new file called **INPUTS_HUAWEI-MIB.conf** should have been created.

Move the generated conf file to the telegraf.d folder, test it is ok and then restart the telegraf service.


## Example 4

This is even more complicated. This MIB file has dependencies.

This is for a CISCO-VTP

``` bash
curl -s ftp://ftp.cisco.com/pub/mibs/v2/CISCO-VTP-MIB.my > CISCO-VTP-MIB.my
```

This MIB requires 2 other MIBs, so also download them. The script won't work otherwise.

``` bash
curl -s ftp://ftp.cisco.com/pub/mibs/v2/CISCO-TC.my > CISCO-TC.my
curl -s ftp://ftp.cisco.com/pub/mibs/v2/CISCO-SMI.my > CISCO-SMI.my
```

Now place all 3 files into one of the mib search paths. I will use */usr/share/snmp/mibs/*

``` bash
cp CISCO-SMI.my /usr/share/snmp/mibs/
cp CISCO-TC.my /usr/share/snmp/mibs/
cp CISCO-VTP-MIB.my /usr/share/snmp/mibs/
```

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/CISCO-VTP-MIB.my 1.3.6.1.2
```

A new file **INPUTS_CISCO-VTP-MIB.conf** should have been created.

Move the generated conf file to the telegraf.d folder, test it is ok and then restart the telegraf service.

## Important

Note that all scalars and tables that are found will be added to the generated configuration file. This may be a lot, so you should decide which elements are important for your needs based on the devices official documentation. Using all scalars(fields) and tables may put unnecessary strain on your server resources and the SNMP device it is querying, so it is important to be sure to delete any fields and tables from the generated conf that you don't actually need.

## Further Notes

You need to tell it which MIB file you want to convert and which base OID to start translating from.

Selecting which Base OID to use will take some research.

I suggest doing an *snmptranslate* on the MIB file first, and select one of the Base OIDs returned.(see below)

If you choose a Base OID to close to the root, it will result in a larger configuration file being generated.

If you choose an OID to specific, then the script may error, or your generated template will contain no useful fields or tables.

eg, 

This produces a very small configuration file with almost no useful information.

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/CISCO-VTP-MIB.my 1.3.6.1.2.1.1
```

This is better, but it could be better still, 

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/CISCO-VTP-MIB.my 1.3.6.1.2.1
```

this may be just fine, 

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/CISCO-VTP-MIB.my 1.3.6.1.2
```

this may even be better. Only you can decide.

``` bash
python SNMP2TELEGRAF.py /usr/share/snmp/mibs/CISCO-VTP-MIB.my 1.3.6.1
```

### Example *snmptranslate*

Example *snmptranslate* to find an appropriate OID to start from.

``` bash
snmptranslate -Tz -m /usr/share/snmp/mibs/CISCO-VTP-MIB.my
```

This will produce a lot of MIBs and corresponding OIDs

``` text
"org"                   "1.3"
"dod"                   "1.3.6"
"internet"              "1.3.6.1"
"directory"             "1.3.6.1.1"
"mgmt"                  "1.3.6.1.2"
"mib-2"                 "1.3.6.1.2.1"
"system"                "1.3.6.1.2.1.1"
"sysDescr"              "1.3.6.1.2.1.1.1"
"sysObjectID"           "1.3.6.1.2.1.1.2"
"sysUpTime"             "1.3.6.1.2.1.1.3"
...
etc
```

From the above response, 

* Using 1.3.6.1.2.1.1 will produce a configuration to small, 
* Using 1.3.6.1.2.1 will produce a better configuration, 
* Using 1.3.6.1.2 will produce an even better configuration with even more coverage.

Only you can decide which you find is more useful for your needs.

Other *snmptranslate* examples

### Ubuntu 18

``` bash
snmptranslate -Tz -m /var/lib/snmp/mibs/ietf/SNMPv2-MIB
```

``` bash
snmptranslate -Tz -m /var/lib/snmp/mibs/ietf/IF-MIB
```

### Centos 7

``` bash
snmptranslate -Tz -m /usr/share/snmp/mibs/SNMPv2-MIB.txt
```

``` bash
snmptranslate -Tz -m /usr/share/snmp/mibs/IF-MIB.txt
```

The correct path of your MIBs files will depend on your OS.
