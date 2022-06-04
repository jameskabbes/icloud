import os
import dir_ops as do

params_Path = do.Path( os.path.abspath(__file__) )
repo_Dir = params_Path.ascend() 
data_Dir = repo_Dir.join_Dir( path = 'Data') 

