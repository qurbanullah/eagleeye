import os
import shutil
import tempfile
import tarfile
import zstandard

from pathlib import Path

from eagleeye.Parse import Parse
from eagleeye.Download import Download


class Package:

    def __init__(self, avouch_packages_download_api_url):
            # self.pkgname = pkgname
            self.avouch_packages_download_api_url = avouch_packages_download_api_url

            self.xml = Parse()

    def verify_package_availability(self, pkgname):
        packge_name = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml", pkgname, 'Name')
        if packge_name:
            return 0
        else:
            return 1


    def verify_package_is_already_installed(self, pkgname):
        pkginfo_path = "/usr/share/avouch/pkginfo"
        package_xml_file = ""+ pkginfo_path +"/"+"".join(pkgname) +".xml"

        if os.path.exists(package_xml_file):
            installed_pkgname = self.xml.get_xml_element_text_from_package_file("Name", package_xml_file)

            if installed_pkgname:
                # print(pkgname, installed_pkgname)
                if pkgname == installed_pkgname:
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 1


    def download(self, package_name):
        packge_name = None
        packge_version = None
        packge_release = None
        packge_distribution = None
        packge_architecture = None
        file_to_download = None
        pkgext_tobeinst = ".avh.tar.zst"
        package_cache_path = "/var/ee/cache"
        

        # xml = ParseXmlFile()

        packge_name = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml", package_name, 'Name')
        packge_version = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml", package_name, 'Version')
        packge_release = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml", package_name, 'Release')
        packge_distribution = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml",package_name, 'Distribution')
        packge_architecture = self.xml.get_xml_element_text_from_package_database_file("/var/ee/db/PackagesDatabase.xml", package_name, 'Architecture')


        file_to_download = packge_name + "-" + packge_version +  "-" + packge_release +  "-" + packge_distribution +  "-" + packge_architecture + pkgext_tobeinst
        file_to_download_url = self.avouch_packages_download_api_url + file_to_download

        # print(package_cache_path + "/" + file_to_download)

        pacage_file_patch = package_cache_path + "/" + file_to_download


        dl = Download()
        dl.download(file_to_download_url, pacage_file_patch)

        # self.install(file_to_download)
        
        return pacage_file_patch


    def extract(self, archive: Path, out_path: Path):
        """extract .zst file
        works on Windows, Linux, MacOS, etc.
        
        Parameters
        ----------
        archive: pathlib.Path or str
        .zst file to extract
        out_path: pathlib.Path or str
        directory to extract files and directories to
        """
        
        if zstandard is None:
            raise ImportError("pip install zstandard")

        archive = Path(archive).expanduser()
        out_path = Path(out_path).expanduser().resolve()
        # need .resolve() in case intermediate relative dir doesn't exist

        dctx = zstandard.ZstdDecompressor()

        with tempfile.TemporaryFile(suffix=".avh.tar") as ofh:
            with archive.open("rb") as ifh:
                dctx.copy_stream(ifh, ofh)
            ofh.seek(0)
            with tarfile.open(fileobj=ofh) as z:
                z.extractall(out_path)


    def copy_files(self, source, destination):
        # os.mkdir(destination)
        # dest_dir = os.path.join(destination,os.path.basename(source))
        # shutil.copytree(source, dest_dir)
        # distutils.dir_util.copy_tree(source, destination)        
        os.system("cp -rf " + source + "/*" + " " + destination)


    def install_dependancy(self, dependancy):       

        if  self.verify_package_availability(dependancy) != 1:
            # print("package is available")

            if  self.verify_package_is_already_installed(dependancy) != 0:
                pkginfo_path = "/usr/share/avouch/pkginfo"
                packge_dependancies = self.xml.get_xml_element_text_array_from_package_database_file("/var/ee/db/PackagesDatabase.xml", dependancy, 'Dependancy')

                print(packge_dependancies)
                # install dependancies
                for dep in packge_dependancies:
                    self.install_dependancy(dep)

                # install actual packages
                print("Downloading package...")
                package_file = self.download(dependancy)

                tempdir = tempfile.mkdtemp()
                print("Extracting package...")
                self.extract(package_file, tempdir)

                print("Copying package files...")
                self.copy_files(tempdir, "/")

                # print(""+ pkginfo_path +"/"+"".join(self.pkgname) +".xml")
                if os.path.exists(""+ pkginfo_path +"/"+"".join(dependancy) +".xml"):
                    print("Package installed successfuly")
                    shutil.rmtree(tempdir)  
                    return 0

                else:
                    print("Error installing package")
                    shutil.rmtree(tempdir)  
                    return 1            
            else:
                print(dependancy, "is already installed")
                return
        else:
            print(dependancy, "is not available")


    def install(self, pkgname):
        
        if  self.verify_package_availability(pkgname) != 1:
            # print("package is available")

            if  self.verify_package_is_already_installed(pkgname) != 0:
                pkginfo_path = "/usr/share/avouch/pkginfo"
                packge_dependancies = self.xml.get_xml_element_text_array_from_package_database_file("/var/ee/db/PackagesDatabase.xml", pkgname, 'Dependancy')

                print(packge_dependancies)
                # install dependancies
                for dep in packge_dependancies:
                    self.install_dependancy(dep)

                # install actual packages
                print("Downloading package...")
                package_file = self.download(pkgname)

                tempdir = tempfile.mkdtemp()

                print("Extracting package...")
                self.extract(package_file, tempdir)

                
                print("Copying package files...")
                self.copy_files(tempdir, "/")

                # print(""+ pkginfo_path +"/"+"".join(self.pkgname) +".xml")
                if os.path.exists(""+ pkginfo_path +"/"+"".join(pkgname) +".xml"):
                    print("Package installed successfuly")
                    shutil.rmtree(tempdir)   
                    return 0

                else:
                    print("Error installing package")
                    shutil.rmtree(tempdir)
                    return 1

                       
            else:
                print(pkgname, "is already installed")
                return
        else:
            print(pkgname, "is not available")

    def remove(self, pkgname):
        if  self.verify_package_is_already_installed(pkgname) == 0:
            pkginfo_file = "/usr/share/avouch/pkginfo/" + pkgname +".xml"
            installed_files = self.xml.get_xml_element_text_array_from_package_info_file(pkginfo_file, 'File')
            # print(installed_files)
            # install dependancies
            print("Removing package...")
            for dep in installed_files:
                print("Removing: ", dep)
                os.remove(dep)

            # print(""+ pkginfo_path +"/"+"".join(self.pkgname) +".xml")
            if os.path.exists(pkginfo_file):
                print("Error removing package")
                return 1
            else:
                print("Package removed successfully")
                return 0                       
        else:
            print(pkgname, "is not installed")
            return