import sys
import requests

from tqdm import tqdm

class Download:

    def __init__(self):
        self
    

    def download(self, url, filename):
        # with open(filename, 'wb') as f:
        #     response = requests.get(url, stream=True)
        #     total = response.headers.get('content-length')

        #     if total is None:
        #         f.write(response.content)
        #     else:
        #         downloaded = 0
        #         total = int(total)
        #         for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
        #             downloaded += len(data)
        #             f.write(data)
        #             done = int(50*downloaded/total)
        #             sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
        #             sys.stdout.flush()
        # sys.stdout.write('\n')

        # credit https://github.com/sirbowen78/lab/blob/master/file_handling/dl_file1.py
        # Home directory of Mac, pathlib.Path module make this easy.
        # home_path = Path.home()
        # This is the sub directory under home directory.
        # sub_path = "tmp"
        # The download link of python.
        # url = "https://www.python.org/ftp/python/3.8.5/python-3.8.5-macosx10.9.pkg"

        # The header of the dl link has a Content-Length which is in bytes.
        # The bytes is in string hence has to convert to integer.
        # print (url)
        filesize = int(requests.head(url).headers["Content-Length"])

        # os.path.basename returns python-3.8.5-macosx10.9.pkg,
        # without this module I will have to manually split the url by "/"
        # then get the last index with -1.
        # Example:
        # url.split("/")[-1]
        # filename = os.path.basename(url)

        # make the sub directory, exists_ok=True will not have exception if the sub dir does not exists.
        # the dir will be created if not exists.
        # os.makedirs(os.path.join(home_path, sub_path), exist_ok=True)

        # The absolute path to download the python program to.
        # dl_path = os.path.join(home_path, sub_path, filename)
        chunk_size = 1024

        # Use the requests.get with stream enable, with iter_content by chunk size,
        # the contents will be written to the dl_path.
        # tqdm tracks the progress by progress.update(datasize)
        with requests.get(url, stream=True) as r, open(filename, "wb") as f, tqdm(
                unit="B",  # unit string to be displayed.
                unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
                unit_divisor=1024,  # is used when unit_scale is true
                total=filesize,  # the total iteration.
                file=sys.stdout,  # default goes to stderr, this is the display on console.
                desc=filename.split("/")[-1]  # prefix to be displayed on progress bar. split the url by "/" then get the last index with -1.
        ) as progress:
            for chunk in r.iter_content(chunk_size=chunk_size):
                # download the file chunk by chunk
                datasize = f.write(chunk)
                # on each chunk update the progress bar.
                progress.update(datasize)

