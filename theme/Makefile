640_480   = installer/cdrom/isolinux/splash.png
1024_768  = installer/cdrom/boot/grub/themes/splash.png
1024_768 += installer/cdrom/assets/usr/share/plymouth/themes/superquinquin/splash.png

SPLASH = $(640_480) $(1024_768)
THEMES = theme/splash-640x480.png theme/splash-1024x768.png
SVGURL = https://www.superquinquin.fr/wp-content/themes/superquinquin/img/superquinquin_logo_deule.svg

# The selected entry background is rendered by GRUB using a **9-slice**
# mechanism: 9 PNG images of 1×1 pixel covering positions `c nw n ne w e sw s # se`.
# All tiles share the same gold color "#f6d443", producing a solid rectangle
# with no rounded corners.
GRUBTHEMEBG  = installer/cdrom/boot/grub/themes/bg
GRUBMAP      = c nw n ne w e sw s se
GRUBMAPFILES = $(GRUBMAP:%=$(GRUBTHEMEBG)/select_%.png)

.INTERMEDIATE: $(SPLASH) $(GRUBMAPFILES)

theme/splash-1024x768.png:
	magick -size 1024x768 xc:white \( $(SVGURL) -resize 320x320 -trim \) \
        -gravity South -geometry +0+50 -composite PNG24:$@

theme/splash-640x480.png:
	magick -size 640x480 xc:white \( $(SVGURL) -resize 200x200 -trim \) \
        -gravity South -geometry +0+40 -composite PNG8:$@

installer/%/splash.png: $(THEMES)
	$(if $(filter $@,$(640_480)),cp theme/splash-640x480.png $@)
	$(if $(filter $@,$(1024_768)),cp theme/splash-1024x768.png $@)

theme/select.png:
	magick -size 1x1 xc:"#f6d443" PNG24:$@

$(GRUBTHEMEBG):
	@mkdir -p $@

$(GRUBTHEMEBG)/select_%.png: theme/select.png $(GRUBTHEMEBG)
	cp $< $@
