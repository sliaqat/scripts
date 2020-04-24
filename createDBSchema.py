import sqlite3, os, sys

# script that creates a sqlite db with table schema based on input csv file. 
# after schema creation, the data from csv file is loaded into the sqlite database
# Usage: 
#      python createDBSchema.py /path/to/file.csv

# Static configuration for script
dbfile="task.db"    # the file name of db that will be created

def load_data(lines):
    """
        function that inserts csv data into the database
        input = lines of csv as list
    """
    try:
        conn = sqlite3.connect(dbfile)
        cur = conn.cursor()

        for line in lines:
            sql = "INSERT INTO task_data VALUES(%s);" % ','.join("'{0}'".format(val) for val in line)
            cur.execute(sql)
            conn.commit()

        print("Data loaded successfully... %s records inserted " % str(len(lines)))
        conn.close()
    except Exception as e:
        print("Error occured during data insertion.. \n")
        print(e)

def create_db(db_schema):
    """
        function that creates the sqlite db file and creates the schema based on csv.
        input = dictionary having fieldname:fieldtype
    """
    try:
        # if db file already exists, drop it
        if os.path.isfile(dbfile):
            print("db file already exists , removing it .. \n")
            os.remove(dbfile)
        # create fields for table creation from the schema read in csv file
        fields = []
        for key,value in db_schema.items():
            fields.append(key + " " + value)

        # create sql statement using fields generated above 
        sql = "CREATE TABLE task_data (%s)" % ",".join(fields)
        print("Create Statement : %s " % sql)
        
        conn = sqlite3.connect(dbfile)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()    

        # also create table for logging
        sql = "Create table log_data (datetime TEXT, msg TEXT)"
        cur.execute(sql)
        conn.commit()    

        print("DB and Schema created Successfully")

        # close the connection
        conn.close()
        
        # return 0 to mark successful completion of method
        return 0
    
    except Exception as e:
        print("Error occured in DB creation")
        print(e)
        return -1
    
def main():
    # dictionary variable to store field names and data types
    db_schema={}

    if not len(sys.argv) > 1:
        print("No CSV filename specified")
        print("kindly run the script with csv filename as \n ./create_and_load_db.py <filename>.csv")
        sys.exit()

    # if above check passes, check if file exists.
    if not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
        print("filename entered either does not exists or is a directory")
        print("please enter the correct filename")
        sys.exit()

    # checks passed, create schema based on file.

    # read file
    f = open(sys.argv[1],'r')

    # create a list of lines in file
    lines = [line.replace('\n','').split(',') for line in f]        

    ### For Schema creation
    # read header , these will become the column names
    header=lines.pop(0)
    
    # from the first line, for simplicity all field types are set to TEXT
    # this process can be modified to detect and set fieldtypes based on data read from first set of values in csv file
    for i in range(0,len(header)):
        fieldname=header[i]
        fieldtype = "TEXT"

        # create dictionary of field names and types 
        db_schema[fieldname]=fieldtype
        
    print("Schema detected as : " )
    print(db_schema)
    # create the schema based on input file.    
    result = create_db(db_schema)

    if result == 0:
        # previous step succeded
        print("Starting the load process for file %s .." % sys.argv[1])
        # load input file data into database
        load_data(lines)
        
if __name__ == "__main__":
    main()
