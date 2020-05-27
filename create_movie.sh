#!/bin/bash

# ffmpeg -r 30 -i plots/spheres/All/all_parts_animation_reg00_snap010_z005p000_angle%05d.png -c:v libvpx-vp9 -b:v 16M -threads 8 movies/sphere_rotate_parttype1_reg00_z005p000.mp4

ptype=1

infile="plots/spheres/All/all_parts_animation_reg00_snap010_z005p000_ptype${ptype}_angle%05d.png"
outfile="movies/sphere_rotate_parttype${ptype}_reg00_z005p000.mp4"

ffmpeg -r 30 -i $infile -c:v mpeg4 -b:v 16M -threads 8 $outfile -vsync 0

