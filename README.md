# Reverse Image Search
Forgot where you left the original of that beautiful photo? If you still have the thumbnail, you can try to find it using Reverse Image Search!

### Installation
```
pip install reverse-image-search
```

### Usage
```bash
$ reverse_image_search images/hills-2836301_1920_thumbnail.jpg images/
Finding similar images...
- to: images/hills-2836301_1920_thumbnail.jpg
- in: images
- filetypes: ['.jpg', '.jpeg']
- threshold: 0.9

Matches:
filepath                                 similarity
---------------------------------------  ------------
images/hills-2836301_1920_thumbnail.jpg  100%
images/hills-2836301_1920.jpg            99%

```

### How does it work?
1. load the image you want to search for.
2. Walk through your files at a given path.
3. Compares the structural similarity between images using Scikit-Image.
4. Print the results in a table when the similarity is above a certain threshold.


### Credits
Image from https://pixabay.com/photos/hills-india-nature-kodaikanal-2836301/
