#!/bin/bash

# convert movie/*.png -delay 10 -morph 10 movie/%05d.morph.png

ffmpeg -r 30 -i movie_images/stars_test_zoom_p03_r_%03d.png -c:v mpeg4 -b 8000k output/stars_test_zoom_p03_r.avi
# -vf "minterpolate=fps=30"
# -qscale 2 
# 

