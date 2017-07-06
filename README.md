# BabyZebras Read Me

Login to pachy using your credentials. 
On windows you can use putty, on Mac/Ubuntu/*nix you can use the default terminal to `SSH`.
## TMUX
You use tmux to basically keep running something on the background. So that even after exiting the prompt (or even logging off a remote machine) you do not break a script.  
More about tmux on: https://en.wikipedia.org/wiki/Tmux  
tmux cheat sheet : https://gist.github.com/MohamedAlaa/2961058

Things we are going to use:

``tmux new -s <session_name>``  *Choose any session name you like (preferably without spaces), this will start a new tmux terminal, anything you do remains within this new virtual terminal*

``Control(both mac and windows) + B, then D`` *will take you out of the tmux. Remember that whatever you are running in that virtual terminal is still running. You simply detached from that session.*

``tmux attach -t <session_name>`` To go back to the same session. 


## Running an instance of pachy (one time setup): 
**Not everyone can run an instance of pachy directly. For permission issues contact admin.**

* Login to pachy
* Create a new TMUX session  
`tmux new -s ibeis_5001`
* Inside the tmux session, go to the directory where you want to create your instance. The preferred directory is `/home/shared_ibeis/data/work/  `
```bash
cd /home/shared_ibeis/data/work    
mkdir BABYMOM    
python2.7 /opt/ibeis/ibeis/dev.py --dbdir /home/shared_ibeis/data/work/BABYMOM/ --web --port 5001
```  
*Any images you upload will now go inside the above directory.*
After you execute the above steps a web instance is setup and you can access the web interface from https://pachy.cs.uic.edu:5001

## Getting copy of a code to pachy:
Clone this GIT repository to your machine and also your home directory on pachy. *Let the admin know if you are unable to clone.*  
``git clone https://github.com/CompBioUIC/BabyZebras``  
You can directly make changes to the code on pachy and run it from there. 


## Uploading images to pachy
The script UploadAndDetectIBEIS.py has all the required methods to upload images to pachy. 
Steps to upload: 
* Create a new script file locally on your computer with the below snippet:
```python
import UploadAndDetectIBEIS as UD
import json

def __main__():
    list_of_images_to_be_uploaded = [this list will contain full paths to the images you want to upload]
    img_file_gid_map = {} # this is the mapping that stores the mapping between the image file and the GID*.
    for img in list_of_images_to_be_uploaded:
    	img_file_gid_map[img] = UD.upload(img)

    with open("name of the mapping file", "w") as mapping_fl:
    	json.dump(img_file_gid_map, mapping_fl, indent=4)

 if __name__ == "__main__":
 	__main__()
```



### Notes:
* GID is nothing but the an ID assigned by the Wildbook to each individual image. A GID uniquely identifies an image. 