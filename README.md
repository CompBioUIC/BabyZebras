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

Clone this GIT repository to your machine and also your home directory on pachy. *Let the admin know if you are unable to clone.*  

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

## Running detection - Recognizing bounding boxes and species of the animal in the bounding box
UploadAndDetectIBEIS.py has the methods to run detection on the images that are uploaded to an instance running.  
You can run these steps only when your upload step is complete.  
Steps to trigger detection module:
* Download UploadAndDetectIBEIS.py to your local computer and add the below code snippet to the code.
```python
def __main__():
    gidList = [i for i in range(start_gid, end_gid+1)] 
    detect = partial(run_detection_task)

    with closing(Pool(processes=2)) as p:
        p.map(detect, gidList)
        p.terminate()
        
if __name__ == "__main__":
    __main__()
```
*start_gid and end_gid specifies for what all gid's you want to run the detection for.*
* Login to pachy 
* Start a new tmux session 
* Simply run 
`python UploadAndDetectIBEIS.py`
* Close the tmux session.
* Exit pachy.
* To check progress you can login back to pachy and attach to the tmux session you created. 


## Running identification pipeline - Recognizing individuals across different images
Identification pipeline unlike detection pipeline looks at annotations instead of images themselves. Each annotation is uniquely identified with a unique ID - AID. Each new annotation is matched against existing annotations in the database. (There is a little bit more to the logic - not every annotation but to the "exemplar" ones). We will do a cold start here since our database is empty.
*We only specify end_gid and identification pipeline will run through gid 1 through end_gid*
* Download UploadAndDetectIBEIS.py to your local computer and add the below code snippet to the code. (You should remove the above snippet(from detection) from the file before running)
```python
def __main__():
    run_id_pipeline(end_gid, 'species for which you are running the detection') # zebra_plains, zebra_grevys, giraffe_reticulated etc. are some of the supported species. 
        
if __name__ == "__main__":
    __main__()
```
* Login to pachy 
* Start a new tmux session 
* Simply run 
`python UploadAndDetectIBEIS.py`
* Close the tmux session.
* Exit pachy.
* To check progress you can login back to pachy and attach to the tmux session you created. 

### Notes:
* GID is nothing but the an ID assigned by the Wildbook to each individual image. A GID uniquely identifies an image. 
