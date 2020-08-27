#!/bin/bash

# ffmpeg -r 30 -i plots/spheres/All/all_parts_animation_reg00_snap010_z005p000_angle%05d.png -c:v libvpx-vp9 -b:v 16M -threads 8 movies/sphere_rotate_parttype1_reg00_z005p000.mp4

ptype=1

infile="plots/parent_zoom/parent_zoom_%03d.png"
outfile="movies/parent_zoom.mp4"

ffmpeg -r 30 -i $infile -c:v mpeg4 -b:v 16M -threads 8 $outfile -vsync 0

