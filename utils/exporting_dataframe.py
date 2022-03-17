from pathlib import Path
import pandas

# only works with the aboslute path C:\Users\jorpa\Documents\ESAN\twitter_fakeNews\data
def export_to_excel(df, path, column):
    # path without "/"
    splitted_path = path.split("/")[6:] # the 6 is an special case for this local pc
    root_path     = path.split("/")[:6]
    # path without "data/"
    creation_path = '/'.join(root_path) + '/clean data/' + '/'.join(splitted_path[1:])
    # path without the name of the file 
    new_path      = '/'.join(root_path) + '/clean data/' + '/'.join(splitted_path[1:-1])
    
    # create the directory if this does not exist
    Path(new_path).mkdir(parents=True, exist_ok=True)
    
    # export the df into the creation_path
    df[column].to_excel(creation_path, sheet_name='Tweets')