# file-watch

Small script to run a file watcher on a set of (sub)folders.
Works as module or from the command line.

When multiple paths are passed a each patch watcher is run in a dedicated thread. 

```
main.py C:/path/to/folder
```

log file is created to log file changes. Currect code filters on gef and ags files being created.

To do:
- [ ] Make file filter dynamic
- [ ] Make file operation filter dynamic
