from jupyter_core.paths import jupyter_data_dir
import subprocess
import os
import errno
import stat

c = get_config()
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.allow_root = True
c.NotebookApp.allow_origin = '*'
# c.NotebookApp.certfile = '/certs/public.pem'
# c.NotebookApp.keyfile = '/certs/tls.key'
c.NotebookApp.open_browser = False
c.NotebookApp.password = ''
c.NotebookApp.token = ''

# Configuration file for jupyter-notebook.
# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False
