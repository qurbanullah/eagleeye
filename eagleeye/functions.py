import os
import subprocess
import json
import zstandard

from pathlib import Path
import tempfile
import tarfile
import xml.etree.ElementTree as ET

class Functions:

    def __init__(self):
        self
        
    def check_for_sudo_privilege(self):
        if (os.geteuid() == 0 and os.geteuid() == os.getuid()):
            # We might have elevated privileges beyond that of the user who invoked
            # the program, due to suid bit. Be very careful about trusting any data! 
            # sudo priveledge is granted            
            return 0
        elif (os.geteuid() != 0 or os.geteuid() != os.getuid()):
            ret = 0
            msg = "[sudo] password for %u:"
            ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)     

            if ret == 0:
                return 0
            else:
                # sudo priveledge is not granted
                return 1             
        else:
            # sudo priveledge is not granted
            return 1

    def verify_package_is_already_installed(self, pkgname, installed_pkgname):
        print(pkgname, installed_pkgname)
        if pkgname == installed_pkgname:
            return 0
        else:
            return 1

    def get_json_property_from_file(self, json_file, json_property):
        # open json file
        f = open(json_file)

        # return json object as a dictionary
        data = json.load(f)
        for prop in data:
            print(prop["name"])

    def get_xml_node_from_file(self, xml_file, xml_root, xml_node):
    # def get_xml_node_from_file(self, xml_file, xml_root):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        node = "./"+"".join(xml_root) +"/Package/"+"".join(xml_node) +""
        # node = "./"+"".join(xml_root) +"/Package/"+""
        # print(node)
        # data = root.findall(node)
        # return data.attrib
        # data = []
        # for child in root.findall(node):
        #     data[child.tag, child.text]

        # print(root.findall(node))

        for child in root.findall(node) :
            # data.append({child.tag, str(child.text)})
        # return data
            return child.text
            

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
