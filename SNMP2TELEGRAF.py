# Copyright 2020 Sean Bradley https://sbcode.net/grafana/

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import re
from io import StringIO
import csv

if(not os.path.exists("snmp2zabbix.conf")):
    MIB2C_CONFIG = """#Copyright 2020 Sean Bradley https://sbcode.net/zabbix/
#Licensed under the Apache License, Version 2.0
@open -@
@foreach $s scalar@
*** scalar, $s, $s.decl, $s.objectID, $s.module, $s.parent, $s.subid, $s.enums, "$s.description" ***
    @foreach $LABEL, $VALUE enum@
*** enum, $LABEL, $VALUE, " " ***
    @end@
@end@
@foreach $t table@
*** table, $t, $t.decl, $t.objectID, $t.module, $t.parent, $t.subid, $t.enums, "$t.description" ***
    @foreach $i index@
*** index, $i, $i.decl, $i.objectID, $i.module, $i.parent, $i.subid, $i.enums, "$i.description" ***
        @foreach $LABEL, $VALUE enum@
*** enum, $LABEL, $VALUE, " " ***
        @end@
    @end@
    @foreach $i nonindex@
*** nonindex, $i, $i.decl, $i.objectID, $i.module, $i.parent, $i.subid, $i.enums, "$i.description" ***
        @foreach $LABEL, $VALUE enum@
*** enum, $LABEL, $VALUE, " " ***
        @end@
    @end@
@end@
"""

    with open("snmp2telegraf.conf", "w") as mib2c_config_file:
        mib2c_config_file.write(MIB2C_CONFIG)


MIB_FILE = sys.argv[1]
BASE_OID = sys.argv[2]
MIB2C_DATA = os.popen('env MIBS="+' + MIB_FILE +
                      '" mib2c -c snmp2telegraf.conf ' + BASE_OID).read()
# print(MIB2C_DATA)
# exit()

MIB_NAME = os.path.basename(MIB_FILE).split(".")[0].replace(" ", "_")
SCALARS = []
ENUMS = {}
LAST_ENUM_NAME = ""  # the one that is being built now
TABLES = {}
LAST_TABLE_NAME = ""  # the one that is being built now

# DATATYPES = {
#     "U_LONG": "int",  
#     "U64": "int", 
#     "OID": "CHAR",
#     "U_CHAR": "CHAR",
#     "LONG": "FLOAT",
#     "CHAR": "TEXT",
#     "IN_ADDR_T": "TEXT"
# }


def getDataType(s):
    dataType = "TEXT"
    return dataType
    # if s.upper() in DATATYPES:
    #     dataType = DATATYPES[s.upper()]
    # else:
    #     print("Unhandled data type [" + s + "] so assigning TEXT")
    # if len(dataType) > 0:  # if data type is INTEGER or other unsigned int, then don't create the node since zabbix will assign it the default which is already unsigned int
    #     return dataType
    # else:
    #     return None


def removeColons(s):
    return s.replace("::", " ")


it = re.finditer(r'\*\*\* (.*[^\*\*\*]*) \*\*\*', MIB2C_DATA)
for l in it:
    line = l.groups()[0]
    groups = re.search(r'.*("[^"]*")', line)
    description = ""
    if groups is not None:
        if groups.group(1) is not None:
            description = groups.group(1).encode('string_escape')
            #description = description.replace('"', '')
            #description = description.replace('\\n', '&#13;')
            description = re.sub(r"\s\s+", " ", description)

    f = StringIO(u'' + line + '')
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if len(row) > 0:
            try:
                if row[0] == "scalar":
                    #print("scaler:\t" + row[4].strip() + "::" + row[1].strip() + "\t" + row[3].strip() + ".0")
                    scalar = [row[4].strip() + "::" + row[1].strip(), row[3].strip() +
                            ".0", getDataType(row[2].strip()), description]
                    SCALARS.append(scalar)
                    LAST_ENUM_NAME = row[4].strip() + "::" + row[1].strip()
                elif row[0] == "table":
                    #print("table:\t" + row[4].strip() + "::" + row[1].strip() + "\t" + row[3].strip())
                    table = [
                        row[4].strip() + "::" + row[1].strip(), row[3].strip(), [], description]
                    if not row[4].strip() + "::" + row[1].strip() in TABLES:
                        TABLES[row[4].strip() + "::" +
                                        row[1].strip()] = []
                    TABLES[row[4].strip() + "::" +
                                    row[1].strip()].append(table)
                    LAST_TABLE_NAME = row[4].strip(
                    ) + "::" + row[1].strip()
                elif row[0] == "enum":
                    #print("enum:\t" + row[1].strip() + "=" + row[2].strip())
                    if LAST_ENUM_NAME not in ENUMS:
                        ENUMS[LAST_ENUM_NAME] = []
                    ENUMS[LAST_ENUM_NAME].append([row[1].strip(), row[2].strip()])
                elif row[0] == "index":
                    #print("index:\t" + row[4].strip() + "::" +
                    #      row[1].strip() + "\t" + row[3].strip())
                    pass
                elif row[0] == "nonindex":
                    #print("nonindex:\t" + row[4].strip() + "::" + row[1].strip() + "\t" + row[3].strip())
                    if int(row[7]) == 1:
                        # print(row)
                        #print("is an enum title : " + row[4].strip() + "::" + row[1].strip())
                        LAST_ENUM_NAME = row[4].strip() + "::" + row[1].strip()
                        column = [row[4].strip() + "::" + row[1].strip(), row[3].strip(),
                                getDataType(row[2].strip()), description, LAST_ENUM_NAME]
                        TABLES[LAST_TABLE_NAME][0][2].append(
                            column)
                    else:
                        # print(row)
                        column = [row[4].strip() + "::" + row[1].strip(),
                                row[3].strip(), getDataType(row[2].strip()), description]
                        # print(description)
                        # print(len(TABLES[LAST_TABLE_NAME][0][2]))
                        TABLES[LAST_TABLE_NAME][0][2].append(
                            column)
                # else:
                #     print("not handled row")
                #     print(row)
            except KeyError:
                print("KeyError Exception.\nThis tends to happen when your Base OID is to specific or not found within the MIB file you are converting.\nChoose a Base OID closer to the root.\nEg, If you used 1.3.6.1.4.1, then try 1.3.6.1.4.\nIf the error still occurs, then try 1.3.6.1.\nNote that using a Base OID closer to the root will result in larger template files being generated.")
                exit()


CONF =  """[[inputs.snmp]]
  agents = [\"udp://127.0.0.1:161\"]
  #timeout = "5s"
  version = 2
  community = "public"
  #retries = 3
  #max_repetitions = 10
  interval = "1m"
  
"""

# SCALARS
for s in SCALARS:
    CONF += """  [[inputs.snmp.field]]
    # """ + s[3] + """
    oid = \"""" + s[1] + """\"
    name = \"""" + s[0] + """\"

"""

# TABLES
if len(TABLES):
    for x in TABLES:
        CONF += """  [[inputs.snmp.table]]
    # """ + TABLES[x][0][3] + """
    oid = \"""" + TABLES[x][0][1] + """\"
    name = \"""" + TABLES[x][0][0] + """\"

"""

# print(CONF)
with open("INPUTS_" + MIB_NAME + ".conf", "w") as conf:
    conf.write(CONF)

print("Done")
