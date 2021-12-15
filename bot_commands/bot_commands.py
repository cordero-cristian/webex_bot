from logging_functions.logger import logger
from netdb.netdb_functions import netdb_functions
import pandas as pd

class bot_commands():

    def __init__(self):
        self.logger = logger()
        self.netdb = netdb_functions()

    def details(self, hostname):
        self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
        obj = self.netdb.execute_raw_sql(
            self.netDbLogOn,
            f"select * from cmdb_mgmt where hostname = '{hostname}'"
        )
        dataFrame = pd.DataFrame.from_records(obj, columns=self.netdb.column_names)
        returnText = dataFrame.to_markdown()
        return returnText
    
    # def running_connfig(self, hostname):
    #     self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
    #     obj = self.netdb.execute_raw_sql(
    #         self.netDbLogOn,
    #         "select hostname, run_config, last_seen "
    #         "from net_config_data.run_config "
    #         f"where hostname = '{hostname}'"
    #     )
    #     return obj
    
    def em7(self, hostname):
        self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
        obj = self.netdb.execute_raw_sql(
            self.netDbLogOn,
            "select * "
            "from net_external.sl1_devices "
            f"where hostname = '{hostname}' or name = '{hostname}'"
        )
        dataFrame = pd.DataFrame.from_records(obj, columns=self.netdb.column_names)
        dataFrame.dropna(inplace=True, axis='columns')
        returnText = dataFrame.to_markdown()
        return returnText

    def interface(self, hostname, interface):
        returnText = ''
        self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
        if interface == None:
            obj = self.netdb.execute_raw_sql(
                self.netDbLogOn,
                "select interface "
                "from net_config_data.interface "
                f"where hostname = '{hostname}'"
            )
        else:
            obj = self.netdb.execute_raw_sql(
                self.netDbLogOn,
                "select * "
                "from net_config_data.interface "
                f"where hostname = '{hostname}' and "
                f"interface = '{interface}'"
            )
        dataFrame = pd.DataFrame.from_records(obj, columns=self.netdb.column_names)
        dataFrame.dropna(inplace=True, axis='columns')
        returnText = dataFrame.to_markdown()
        return returnText
    
    def snmp(self, hostname):
        self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
        obj1 = self.netdb.execute_raw_sql(
            self.netDbLogOn,
            "select * "
            "from net_config_data.snmp_community "
            f"where hostname = '{hostname}'"
        )
        dataFrame1 = pd.DataFrame.from_records(obj1, columns=self.netdb.column_names)
        obj2 = self.netdb.execute_raw_sql(
            self.netDbLogOn,
            "select * "
            "from net_config_data.snmp_settings "
            f"where hostname = '{hostname}'"
        )
        dataFrame2 = pd.DataFrame.from_records(obj2, columns=self.netdb.column_names)
        joinedDataFrame = pd.concat([dataFrame1, dataFrame2], axis=1)
        joinedDataFrame.dropna(inplace=True, axis=1, how='all')
        returnText = joinedDataFrame.to_markdown()
        return returnText

    def vlan(self, hostname, vlan_name):
        returnText = ''
        self.netDbLogOn = self.netdb.data_base_log_on(svc_rw=True)
        if vlan_name == None:
            obj = self.netdb.execute_raw_sql(
                self.netDbLogOn,
                "select vlan_name "
                "from net_config_data.vlan "
                f"where hostname = '{hostname}'"
            )
        else:
            obj = self.netdb.execute_raw_sql(
                self.netDbLogOn,
                "select * "
                "from net_config_data.vlan "
                f"where hostname = '{hostname}' and "
                f"vlan_name = '{vlan_name}'"
            )
        dataFrame = pd.DataFrame.from_records(obj, columns=self.netdb.column_names)
        dataFrame.dropna(inplace=True, axis='columns', how='all')
        returnText = dataFrame.to_markdown()
        return returnText