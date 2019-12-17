#!/bin/bash

ffmpeg  -framerate 15 -i movie_images/gas_test_zoom_1_r_1_p_%03d.png -vf scale=256:144 output/gas_test_zoom_1_r_1.gif

# -vf "minterpolate=fps=30"
# -f image2
