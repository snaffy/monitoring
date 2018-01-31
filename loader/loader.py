import yaml
from operator import attrgetter


class Dbi:
    def __init__(self, instances):
        self.list_in = instances

    def getConfiguration(self):
        for instance in self.list_in:
            type_instance = instance.type_instance
            result = ""
            db_section = ""
            query = ""
            for item in type_instance:
                # TODO mock konfiguracji
                if instance.configuration is None:
                    instance.configuration = {'interval': '300', 'driver': 'mysql', 'host': '127.0.0.1', 'port': '3306',
                                       'username': 'root', 'password': 'RootPassCh1HXKs24'}

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
            configuration = """LoadPlugin dbi
                <Plugin dbi>
                    {conf}
                </Plugin>""".format(conf=result + db_section)
            return configuration

class DbiLoader:

    def __init__(self, name, configuration, type_instance):
        self.type_instance = type_instance
        self.name = name
        self.configuration = configuration

    def load(self):
        list = []
        instance = self['instance']
        for i in instance:
            instance_name = i['name']
            override_conf = i['override_conf']
            type_instance = i['type_instance']
            list.append(DbiLoader(instance_name, override_conf, type_instance))
        return Dbi(list)

with open(
        "D:\\Development\\Python\\monitoring\\monitoring\\loader\\vehicle-event-router-staging-yaml-concept\\dbi_value.yaml") as stream:
    try:
        tmp = (yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

x = DbiLoader.load(tmp)
print(x.getConfiguration())