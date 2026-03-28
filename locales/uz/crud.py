import psycopg2


class DB:
    dbname = "postgres"
    port = 5432
    host = "localhost"
    user = "postgres"
    password = '1'
    connect = psycopg2.connect(dbname=dbname,port=port,host=host,user=user,password=password)
    cursor = connect.cursor()


class CRUD:
    def delete(self):
        table_name = self.__class__.__name__.lower() + "s"
        query = f"""
                    delete from {table_name} where id = %s
                    """
        DB.cursor.execute(query, (self.id,))
        DB.connect.commit()

    def update(self , **kwargs):
        table_name = self.__class__.__name__.lower() + "s"
        set_format = "= %s ,".join(kwargs.keys()) + "= %s "
        query = f"""
            update {table_name} set {set_format} where id = %s
            """
        vals = list(kwargs.values()) + [self.id]
        DB.cursor.execute(query , tuple(vals))
        DB.connect.commit()

    def get_data(self)-> list:

        table_name = self.__class__.__name__.lower() + "s"


        fields = {}
        for field, value in self.__dict__.items():
            if value != None:
                fields[field] = value
        condition_format = "where " + "= %s and ".join(fields.keys()) + "= %s" if fields else ""
        query = f"""
                            select * from {table_name} {condition_format}
                            """
        objects = []

        DB.cursor.execute(query, tuple(fields.values()))
        for data in DB.cursor.fetchall():
            obj = self.__class__(*data)
            objects.append(obj)
        return objects

    def save(self):
        table_name = self.__class__.__name__.lower() + "s"
        fields = {}
        for field , value in self.__dict__.items():
            if value != None:
                fields[field] = value
        field_format = ",".join(fields.keys())
        values_format = ",".join(["%s"]*len(fields.keys()))
        query = f"""
            insert into {table_name} ({field_format}) values ({values_format})
            """
        DB.cursor.execute(query , tuple(fields.values()))
        DB.connect.commit()
