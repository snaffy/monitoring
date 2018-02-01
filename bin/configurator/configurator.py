from bin.loader.loader import DefaultConfig, FileLoader


class DbiParser:
    def __init__(self, name, configuration, type_instance):
        self.type_instance = type_instance
        self.name = name
        self.configuration = configuration

    def pare_data(self):
        fl = FileLoader(self)
        data = fl.getData()
        list = []
        instance = data['instance']
        for i in instance:
            instance_name = i['name']
            if 'override_conf' in i:
                override_conf = i['override_conf']
            else:
                override_conf = None
            type_instance = i['type_instance']
            list.append(DbiParser(instance_name, override_conf, type_instance))
        return DbiConfig(list)



class DbiConfig:
    def __init__(self, instances):
        self.list_in = instances

    def getConfiguration(self):
        conf = ""
        for instance in self.list_in:
            type_instance = instance.type_instance
            result = ""
            db_section = ""
            query = ""
            for item in type_instance:
                if instance.configuration is None:
                    instance.configuration = DefaultConfig.getDefaultDatabaseConfig()
                else:
                    instance.configuration = {**DefaultConfig.getDefaultDatabaseConfig(), **instance.configuration}

                query += """
                 Query "{qry_name}" 
                """.format(qry_name=item['name'])

                result += """
                <Query "{qry_name}">
         	        Statement "{statement} as value"
         	            <Result>
         		            Type "gauge"
         		            InstancesFrom "{qry_name}"
         		            ValuesFrom "value"
         	            </Result>
                </Query> 
                """.format(qry_name=item['name'],
                           statement=item['cnf'])

            db_section += """
                <Database "{database}">
                    Interval {internal}
                    Driver "{driver}"
                    DriverOption "host" "{host}"
                    DriverOption "port" "{port}"
                    DriverOption "username" "{username}"
                    DriverOption "password" "{password}"
                    {qry}
                </Database>
                """.format(database=instance.name,
                           internal=instance.configuration['interval'],
                           driver=instance.configuration['driver'],
                           host=instance.configuration['host'],
                           port=instance.configuration['port'],
                           username=instance.configuration['username'],
                           password=instance.configuration['password'],
                           qry=query)

            conf += result + db_section

        configuration = """LoadPlugin dbi
                        <Plugin dbi>
                              {conf}
                          </Plugin>""".format(conf=conf)
        return configuration


class MysqlMonitorConfig:
    default_data = DefaultConfig.getDefaultMysqlMonitorConfig()

    def __init__(self, path_to_override_conf, host_name):
        self.host_name = host_name
        self.path_to_override_conf = path_to_override_conf

    def getOverrideConfiguration(self):
        fl = FileLoader(self.path_to_override_conf)
        return fl.getData()['override_conf']

    def getConfiguration(self):
        merged_data = {**self.default_data, **self.getOverrideConfiguration()}
        config = """LoadPlugin mysql
        <Plugin mysql>
        	<Database "{db_name}">
        		Host "{host}"
        		Port "{port}"
        		User "{user}"
        		Password "{password}"
        	</Database>
        </Plugin> """.format(host=merged_data['host'],
                             port=merged_data['port'],
                             user=merged_data['user'],
                             password=merged_data['password'],
                             db_name=self.host_name)

        return config


class FileCountConfig:
    def __init__(self, path_to_conf):
        self.path_to_conf = path_to_conf

    def getConfiguration(self):
        fl = FileLoader(self.path_to_conf).getData()
        files = fl.get('Files')
        result =""
        for item in files:
            result += """
            <Directory "{path}" >
 		        Instance "{name}"
 	    	    Name "{name}"
 	        </Directory>
            """.format(path=item['dir_path'],
                       name=item['name'])
        final_result = """
        LoadPlugin filecount 
            <Plugin filecount>
                {conf}
             </Plugin>
        """.format(conf=result)
        return final_result
