#!/usr/bin/env python

import mysql.connector, pyperclip, sys
import config

mydb = mysql.connector.connect(
host = config.db_host,
port= config.db_port,
user = config.db_user,
password = config.db_pswd,
database = config.db_database)

mycursor = mydb.cursor(buffered=True)

value = sys.argv[1]

if len(sys.argv) == 2 and sys.argv[1].isdigit(): #id expected   
    child_id = sys.argv[1]
    mycursor.execute(f"select name from lp_organizations where id={child_id}")
    child_name = [x for x in mycursor][0][0]
  
elif len(sys.argv) == 3: #postcode expected    
    mycursor.execute(f"select name,id from lp_organizations where postcode='{' '.join(sys.argv[1:])}'")
    child_name, child_id = [x for x in mycursor][0]
else:
    raise Exception("Input postcode or org ID.")
    
mycursor.execute(f"""
select lp_organizations.id, lp_organizations.name 
from lp_organizations 
inner join lp_organization_hierarchy ON lp_organizations.id =  lp_organization_hierarchy.parent 
where lp_organization_hierarchy.child = {child_id}
""")
parent_details = [x for x in mycursor]

parent_id = parent_details[0][0]
parent_name = parent_details[0][1]

if config.parent_name not in parent_name: #reseller is the parent
    string = f""" 
Partner Organisation Name: {parent_name}
Partner Portal ID: {parent_id}
Customer Organisation Name: {child_name}
Customer Portal ID: {child_id}
    """
else:
    string = f"""
Customer Organisation Name: {child_name}
Customer Portal ID: {child_id}
    """
pyperclip.copy(string)

print(string)
