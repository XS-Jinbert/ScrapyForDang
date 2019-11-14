# ScrapyForDang

A Spider that crawling The NewYork Times, The Washington Post, Los Angeles Times, Chicago Tribune

----

This is a spider that for crawling articles from four journal above. And what I record is the atrticle's name ,date and content. Apart from that I also write script for limit the time between A and B.And I think it will help some one in someway though it is not perfect, obviously.And I like write down some note to avoid wasting your time.

### Directory Structure

>However from the main.py we can see that the second level directories(CT,TNYT...) will be made one by one rather than at once. It's my fault.

    
    .
    ├── source_dir
    │   ├── CT                    # The abbreviation for Chicago Tribune. The following are the same 
    │   ├── TNYT        
    │   ├── WST
    │   └── LAT
    │   │   ├── article_file.txt  # which including url, date and content
    └── ...
    
### Crawling Procedure Note

> if you don't want to go through the whole project, here's some note you must know and to set the param.

- In `scrapySP/main.py` you should choose which journal you want crawl 

- You should comfirm your save path in `scrapySP/pipelines`

- Some auxiliary functions are made in `helper.py` including the starttime and stoptime 

### The disadavantage 

- I can't crawl four journal at once 

- If you crawl the WST that you will found I use Chrome webdriver with head, cause headless mode cannot work and I can't fix it.In a short you will feel the time is so slow when running the `WST_spider.py` 

- The method for revising date format is alos not wise actually, I just enumerate the format that I have met and fix it.

### END

> If you are sure that you set all path and param right, please run the `main.py`, and you may get the instruction like following:

```
...
2019-11-14 25:60:60 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 000.0.0.0:0000
Please input what you want to search(one by one word)
hello
world
...
```

In the end, Thank you for reading and using, hopfully that I can get any hint from you 

Ego
2019-11-14 




  
