# Scraping Basics
This readme describes steps of scraping images from Flickr and Bing. 
Please install the below dependencies by running the below command directly on your command line. 
*Assuming you have installed `python 3.x`.*

`pip install flickrapi`  
`pip install urllib`

## Using the config file
The file `WebScrapeConfig.xml` has details on where the key file is stored etc. Below is a snippet of the XML file.  
You have to change the parameters depending on where you store the key file, where you want the downloaded files to be stored etc. 

Some comments have been added to the config directly to remind what the parameters mean. Similar parameters exist for `Bing` as well.

```xml
<flickr_config>
    <flickr_api_key_file location="<specify where the flickr key (in JSON form) is stored"></flickr_api_key_file>
    <flickr_download_dir dir="/tmp/"></flickr_download_dir> <!-- directory where you want to store your downloaded images-->
</flickr_config>
```

To start, simply clone this branch using the below command and switch to this current branch. 
```
git clone https://github.com/CompBioUIC/BabyZebras.git
git checkout scraping_branch
```

## Scraping images from Flickr
Open a new file in any text editor and save it as `<filename of your choice>.py` and add the below code snippet. 

```python
import SocialMediaImageExtracts as SE

def __main__():
  SE.scrape_flickr(10, "links.dat", ["grevy's zebra"]) 
  '''
    This step will scrape the first 10 pages of Flickr when you search using the query "grevy's zebra" 
    And then store the URLs of all those images appearing in these 10 pages to output.dat
  '''
  
  SE.download_imgs("links.dat") #this step simply downloads every link in the links.dat file
  

if __name__ == "__main__":
  __main__()

```

## Scraping EXIF data from Flickr
After downloading the images from Flickr and manually filtering the images manually to remove all junk images, we also need to download the metadata or `EXIF` information for each image. EXIF information means date when the image was taken, width-height of the image etc. 

Create a file with list of images that you downloaded and filtered, save it with a name of your choice, say, `imageList.dat`. Create a new file and save it in the folder where you `SocialMediaExtracts.py` exists with the below snippet. 

```python 
import SocialMediaImageExtracts as SE

def __main__():
    configDict = SE.xml_parser()
    
    flickrObj = config_dict["flickr_api_key_file"]
    
    with open("imageList.dat", "r") as fl:
        fileList = fl.read().split("\n")
        
    getExif(flickrObj, <name of output file>.json, fileList = fileList) 
```

This script will give you a JSON file specified as `"<name of the output file>.json"`, we will be using this in the future for population estimation.

## Scraping images from Bing
Similar to what we did for Flickr scrapes, a file with name of your choice and paste the below snippet. 
```python
import SocialMediaImageExtracts as SE

def __main__():
  SE.bing_search_pipeline("grevy's zebra", 10)
  '''
    This step will scrape the first 10 pages of Bing when you search using the query "grevy's zebra" 
    And then also downloads all the images found in the first 10 pages to the download directory you specified in the config file
    
    This script will also generate a bunch of exif files in json form 
    (typically, width & height of the image and when the image was published)
    Look at the DataStructsHelperAPI.py file for help in combining these JSONs into 1 big file. 
  '''

if __name__ == "__main__":
  __main__()

```

## Combining JSONs outputted by the Bing scrape
As you may have already observed, the bing scrape generated a bunch of JSON file in the form `../data/bing_img_exif_giraffe_*` (assuming you kept `<bing_exif_prefix prefix="../data/bing_img_exif_giraffe_"></bing_exif_prefix>` in the config file). 

Below script can be used to combine multiple JSON file into a single JSON.
Assume you have the below JSON files outputted by the bing scraping method.

```
../data/bing_img_exif_giraffe_150.json
../data/bing_img_exif_giraffe_300.json
../data/bing_img_exif_giraffe_450.json
../data/bing_img_exif_giraffe_600.json
```

```python
import DataStructsHelperAPI as DS, json

def __main__():
    combinedDict = DS.appendJSON(../data/bing_img_exif_giraffe_150.json,
                                 ../data/bing_img_exif_giraffe_300.json,
                                 ../data/bing_img_exif_giraffe_450.json,
                                 ../data/bing_img_exif_giraffe_600.json)
                                 
    with open("../data/bing_img_exif_giraffe_cobined.json", "w") as fl:
        json.dump(combinedDict, fl, indent=4)
```

## Expected Errors
The step of downloading is known to fail. We are using 2 processes to simulaneously download images and this can cause network congestion and the script might fail. 
Due to its uncertainity, you might observe it every time you run or never. The best thing you can do is to scrape in small batches. For instance, instead of scraping from 50 pages at once, try first 10 and then move ahead. You might have to make changes to code accordingly. I will add this to my to-do list and see if there is a way to do smooth restarts in case of a failure. 



# Creating a wildbook instance

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
python2.7 /opt/ibeis/ibeis/dev.py --dbdir /home/shared_ibeis/data/work/BABYMOM/ --web --port 5000
```  
*Any images you upload will now go inside the above directory.*
After you execute the above steps a web instance is setup and you can access the web interface from https://pachy.cs.uic.edu:5000

## Getting copy of a code to pachy:
Clone this GIT repository to your machine and also your home directory on pachy. *Let the admin know if you are unable to clone.*  
``git clone https://github.com/CompBioUIC/BabyZebras.git``
``git checkout scraping_branch``
You can directly make changes to the code on pachy and run it from there. 


## Uploading images to pachy
The script UploadAndDetectIBEIS.py has all the required methods to upload images to pachy. 
Steps to upload: 
* Create a new script file locally on your computer with the below snippet:  
**The upload process using the below script will generate a JSON, make sure you save it.**
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
