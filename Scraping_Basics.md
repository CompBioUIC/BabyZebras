# Scraping basics
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
