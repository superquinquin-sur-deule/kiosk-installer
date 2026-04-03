640_480   = installer/cdrom/isolinux/splash.png
1024_768  = installer/cdrom/boot/grub/themes/splash.png
1024_768 += installer/cdrom/assets/usr/share/plymouth/themes/superquinquin/splash.png

SPLASH = $(640_480) $(1024_768)
THEMES = theme/splash-640x480.png theme/splash-1024x768.png
SVGURL = https://www.superquinquin.fr/wp-content/themes/superquinquin/img/superquinquin_logo_deule.svg

.INTERMEDIATE: $(SPLASH)

theme/splash-1024x768.png:
	magick -size 1024x768 xc:white \( $(SVGURL) -resize 320x320 -trim \) \
        -gravity South -geometry +0+50 -composite PNG24:$@

theme/splash-640x480.png:
	magick -size 640x480 xc:white \( $(SVGURL) -resize 200x200 -trim \) \
        -gravity South -geometry +0+40 -composite PNG8:$@

installer/%/splash.png: $(THEMES)
	$(if $(filter $@,$(640_480)),cp theme/splash-640x480.png $@)
	$(if $(filter $@,$(1024_768)),cp theme/splash-1024x768.png $@)
