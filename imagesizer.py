#!/usr/bin/env python

# imagesizer - shrink images to (roughly) the desired filesize
# made with <3 from moth.monster

# SPDX-License-Identifier: MIT-0

import click, os, math
from PIL import Image

Image.MAX_IMAGE_PIXELS = None # jarvis, disable my gigapixel inhibitors

@click.command()
@click.option('-s', '--size', default=100, help='Target output filesize (in kB)')
@click.option('-w', '--webp', is_flag=True, help='If enabled uses WebP, otherwise JPEG')
@click.argument('infile')
@click.argument('outfile', type=click.Path(dir_okay=False, writable=True))
@click.version_option(version='0.1.0', prog_name="imagesizer", message="%(prog)s v%(version)s")

def compress(infile, size, webp, outfile):
	"""Simple tool which shrinks an image to (roughly) the desired filesize."""
	with Image.open(infile) as img:
		img.thumbnail((math.log2(size)*200,(math.log2(size)*200))) # ensure image is somewhat reasonably sized
		if webp: # disgusting brute forcing, but it's Fast Enough™
			for q in range(100, 20, -5):
				img.save(outfile, 'webp', quality=q, alpha_quality=q)
				if os.stat(outfile).st_size <= size*1000:
					break
		else:
			for q in range(90, 10, -5):
				img.save(outfile, 'jpeg', quality=q)
				if os.stat(outfile).st_size <= size*1000:
					break

if __name__ == '__main__':
	compress()