# xkcd_comics_scraper
A script inspired by the Automate the Boring Stuff with Python book, bringing together some of the concepts learned.

The script currently does the following: 

1. open the main page of the xkcd comics
1. get title, hover text, permalink and embed url for current image + link to previous image
1. download image
1. print file name, title, hover text, permalink and embed url
1. save file name, title, hover text, permalink and embed url to .xslx document
1. open previous image page and repeat steps 2 - 5 in the range specified

There are two download options available: specified number of images or all images currently posted on the website. 

The download process starts at the latest posted image.

P.S.: The objective for writing this script was not to create the most efficient tool for downloading all of xkcd comics, but to get some practice with web scraping and using Beautiful Soup. =)
