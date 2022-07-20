import os
import shutil
from datetime import datetime

from .download import Download
from .functions import Functions
from .parse import Parse


class Database:

    def __init__(self, dburl):
        self.url = dburl
        self.xml = Parse()
    

    def update(self):
        packagesDatabaseDirectory = "/var/ee/db/"
        packagesDatabaseArchive = "PackagesDatabase.tar.zst"    
        packagesDatabase = "PackagesDatabase.xml" 

        # pkgdb_url = url
        pkgdb_url = self.url + packagesDatabaseArchive
        pkgdb_archive = packagesDatabaseDirectory + packagesDatabaseArchive
        pkgdb_file = packagesDatabaseDirectory + packagesDatabase

        if os.path.exists(pkgdb_file):
            # print("database exists...")
            # check database is updated or not by checing database date
            database_date = self.xml.get_xml_date_element_text_from_package_database_file(pkgdb_file, 'DatabaseDate')
            
            database_date_time_obj = datetime.strptime(database_date, '%Y-%m-%d %H:%M:%S')

            # print(database_date_time_obj)
            # today = date.today()
            today_date = datetime.today()
            # print(today_date)
            # print(date_time_obj < today_date) #True
            diff_date = today_date - database_date_time_obj
            # print(diff_date)

            now = datetime.now() # current date and time
            date_time = now.strftime("%m-%d-%Y_%H-%M-%S")

            # if difference is greater than 3 days 86400 seconda in 1 day
            # 86400 x 3 259200
            if diff_date.total_seconds() > 259200.0:
                print("Database is too old, updating...")
                # backup the previous database
                shutil.move(pkgdb_file, pkgdb_file + "." + date_time)

                dl = Download()
                dl.download(pkgdb_url, pkgdb_archive)

                func = Functions()
                if os.path.exists(pkgdb_archive):
                    func.extract(pkgdb_archive, packagesDatabaseDirectory)
                else:
                    print("Error extracting database archive")
                    return 1

                if os.path.exists(pkgdb_file):
                    print("Database updated successfully")
                    # delete database archive
                    os.remove(pkgdb_archive)
                    return 0
                else:
                    print("Error updating database")
                    return 1
            else:
                return 0          
        else:
            print("Downloading database...")
            dl = Download()
            dl.download(pkgdb_url, pkgdb_archive)

            func = Functions()
            if os.path.exists(pkgdb_archive):
                func.extract(pkgdb_archive, packagesDatabaseDirectory)
            else:
                print("Error extracting database archive")
                return 1

            if os.path.exists(pkgdb_file):
                print("Database updated successfully")
                # delete database archive
                os.remove(pkgdb_archive)
                return 0
            else:
                print("Error updating database")
                return 1

