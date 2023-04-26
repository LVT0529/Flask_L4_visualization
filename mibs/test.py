from pysnmp.hlapi import *


# SNMP WALK 요청 보내기
for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
        SnmpEngine(),
        CommunityData('skdnzha', mpModel=0),
        UdpTransportTarget(('211.49.171.10', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('F5-BIGIP-GLOBAL-MIB','gtmGlobals ',0)),
        lexicographicMode=False
):
    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
        break
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
