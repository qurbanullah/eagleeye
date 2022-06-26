import sys
import argparse

from Functions import Functions
from Database import Database
from Package import Package

def main():

    pkgname = None
    install_package = 0
    remove_package = 0


    avouch_packages_download_api_url = "https://avouch.org/api/download-package/"
    avouch_packages_info_download_api_url="https://avouch.org/api/download-package-info-file/"
    avouch_packages_database_download_api_url = "https://avouch.org/api/download-package-database/"

    packagesDatabaseDirectory = "/var/avouch/database"
    packagesDatabase = "PackagesDatabase.xml"
    packagesFilesDatabase = "PackagesFilesDatabase.xml"

    installedPackagesDatabase = "/usr/share/avouch/database/InstalledPackagesDatabase.xml"
    installedPackagesFilesDatabase = "/usr/share/avouch/database/InstalledPackagesFilesDatabase.xml"    

    #Initialize
    parser=argparse.ArgumentParser(description="Simple calculator")
    group = parser.add_mutually_exclusive_group(required=True)
     
    #Adding optional parameters
    group.add_argument('--install', '-i',
                        metavar='<package name>',
                        nargs='+',                        
                        type=str,
                        help="Install the given package")
 
    group.add_argument('--remove', '-r',
                        metavar='<package name>',
                        nargs='+',                        
                        type=str,
                        help="Remove the given package")

    group.add_argument('--update', '-u',                      
                        action='store_true',
                        help="Update packages database")

    parser.add_argument('--force', '-f',
                        action='store_true', 
                        help="Force the action")

    # parser.add_argument('source_file', type=open)
 
     
    #Parsing the argument
    args=parser.parse_args()

 
    functions = Functions()
    pkgdb = Database(avouch_packages_database_download_api_url)
    package = Package(avouch_packages_download_api_url)
    
    # Install packge
    if args.install:
        pkgname = args.install
        
        if functions.check_for_sudo_privilege() == 0:
            # update package database first
            pkgdb.update()

            for pkg in pkgname:
                package.install(pkg)                
        else:
            # the user wasn't authenticated as a sudoer, exit?
            print("The user wasn't authenticated as a sudoer")
            sys.exit(1)
 
    # Install packge
    if args.remove:
        pkgname = args.remove

        if functions.check_for_sudo_privilege() == 0:
            for pkg in pkgname:
                package.remove(pkg)                
        else:
            # the user wasn't authenticated as a sudoer, exit?
            print("The user wasn't authenticated as a sudoer")
            sys.exit(1)

    # Update package database
    if args.update:
        print("Updating packages database")

    # Update package database
    if args.force:
        print("Forcing the action")

    # install and remove at same time is not allowed
    if args.install and args.remove:
        print("Installing and removing a package at same time is not alowed")
        sys.exit(1)

if __name__ == '__main__':
    main()