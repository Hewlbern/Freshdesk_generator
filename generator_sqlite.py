from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
from random import randrange
import json
import sqlite3

def ticket_gen(n):
        
        """ This creates a random set of tickets."""  
        
        #This is the different words we'll be using for various generated data sets
        faker = Faker()
        df = []
        meta = {}
        activ = {}
        key = []
        users = ['user', 'admin', 'customer']
        activities = ['note', 'admin', 'customer']
        category = ['Phone', 'computer', 'jackets']
        product = ['mobile', 'tigimon', 'tamigotcha']
        status = ['open', 'closed', 'resolved','waiting for customer', 'waiting for third party', "pending"]
        descr_act = []
        activity = []
        meta_data = []
        for n in range(n):
        
        
            #key.append(n)
            #this creates the intial metadata
            
            #Time is set from the time_origin, which is when the first ticket is made,
            #and then added onto at random intervals 
            
            time_origin = faker.date_time_this_century()
    
            activities = randrange(10)
            work_type  = randrange(1,4)
           
            
            desc_act_mwap ={'key':n,
                         'performed_at': faker.date_time_this_century(),
                         'ticket_id': randrange(80,1000),
                         'performer_type': faker.words(1, users, True)[0],
                         'performer_id': randrange(80,10000) }
            descr_act.append(desc_act_mwap)


            activity_next = time_origin
            for x in range(activities):
                #depending on the total activities, this creates what information is in those activities
                activity_next = activity_next + timedelta(days=randrange(10))

                if work_type == 1:
                    #if the ticket type is note, as per example

                    act_data_note =  {'key':n,'performed_at': activity_next,
                             'id': randrange(80,1000),
                             'category': faker.words(1, category, True)[0],
                             'type': randrange(20)}
                    activity.append(act_data_note)

                    x+=1
                    activity_next = activity_next + timedelta(days=randrange(3))

                else:
                                        #if the ticket type is shipping, as per example

                    act_data_shipping =  {
                        'key':n,
                        'performed_at': time_origin,
                        'shipping_address': faker.address(),
                        'shipping_date': activity_next,
                        'category': faker.words(1, users, True)[0],
                        'priority': randrange(5),
                        'status': faker.words(1, status, True)[0],
                        'contacted_customer': faker.pybool(),
                        'source': randrange(5),
                        'agent_id': randrange(2000),
                        'requester': randrange(2000),
                        'product': faker.words(1, product, True)[0]}
                    activity.append(act_data_shipping)
                    activity_next = activity_next + timedelta(days=randrange(3))



                    x+=1
                    
            meta_data_make = {'key':n,'start_at': time_origin, 'end_at': activity_next,
                                   'activities_count': randrange(100) }
            meta_data.append(meta_data_make)
            
            time_origin = activity_next + timedelta(days=randrange(10))

                    
            #when this loop has finished, we append the generated data to the dataframe.
           # df.append({'metadata': {'key':{n},'start_at': {time_origin}, 'end_at': {activity_next},
                  #                 'activities_count': {randrange(100)} },
              #        'activities_data':[descr_act,activity]})
        act_df = pd.DataFrame(activity)#.set_index(['key'])
        desc_df = pd.DataFrame(descr_act)#.set_index(['key'])
        meta_df = pd.DataFrame(meta_data)#.set_index(['key'])
        return act_df,desc_df,meta_df


act_df,desc_df,meta_df  = ticket_gen(1000)


meta_df.to_json('metadata.json', orient='records', lines=True)
act_df.to_json('activities_data.json', orient='records', lines=True)
desc_df.to_json('description_data.json', orient='records', lines=True)


db=sqlite3.connect('FreshDeskTest.sqlite3')
tablename = ["metadata","activities_data","description_data"]
table_length = len(tablename)

n = 0
for n in range(table_length):
    
    json_data = []
    for line in open(tablename[n]+'.json', 'r', encoding='utf-8-sig'):
        json_data.append(json.loads(line))



    #Aim of this block is to get the list of the columns in the JSON file.
    columns = []
    column = []
    print(columns)
    for data in json_data:
        column = list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)

    #Here we get values of the columns in the JSON file in the right order.   
    value = []
    values = [] 
    for data in json_data:
        for i in columns:
            value.append(str(dict(data).get(i)))   
        values.append(list(value)) 
        value.clear()

    if n == 0:

       #Time to generate the create and insert queries and apply it to the sqlite3 database       
        create_query = "create table if not exists metadata ({0})".format(" text,".join(columns))
        insert_query = "insert into metadata ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))    
        print("insert has started at " + str(datetime.now()))  
        c = db.cursor()   
        c.execute(create_query)
        c.executemany(insert_query , values)
        values.clear()
        db.commit()
        c.close()
        print("insert has completed at " + str(datetime.now())) 
    elif n ==1 :
        #Time to generate the create and insert queries and apply it to the sqlite3 database       
        create_query = "create table if not exists activities_data ({0})".format(" text,".join(columns))
        insert_query = "insert into activities_data ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))    
        print("insert has started at " + str(datetime.now()))  
        c = db.cursor()   
        c.execute(create_query)
        c.executemany(insert_query , values)
        values.clear()
        db.commit()
        c.close()
        print("insert has completed at " + str(datetime.now())) 
    else:
        #Time to generate the create and insert queries and apply it to the sqlite3 database       
        create_query = "create table if not exists description_data ({0})".format(" text,".join(columns))
        insert_query = "insert into description_data ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))    
        print("insert has started at " + str(datetime.now()))  
        c = db.cursor()   
        c.execute(create_query)
        c.executemany(insert_query , values)
        values.clear()
        db.commit()
        c.close()
        print("insert has completed at " + str(datetime.now())) 
    
    n+=1


# Create your connection.
cnx = sqlite3.connect('FreshDeskTest.sqlite3')
df = pd.read_sql_query("SELECT * FROM activities_data", cnx)


