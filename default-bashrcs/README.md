These files are copied during installation process. If each bashrc exists on the filesystem and contains the `source`
to whatever entrypoint they each point to, then these files will not be overwritten by update. The files in this directory should only be edited when modifying distribution files.

To edit your own bashrc:
```
cd /data/community/
ls -al
vi .bashrc
```
