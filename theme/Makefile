640_480   = installer/cdrom/isolinux/splash.png
320_320   = installer/cdrom/boot/grub/themes/splash.png
320_320  += installer/cdrom/assets/usr/share/plymouth/themes/superquinquin/splash.png

SPLASH = $(320_320) $(640_480)
THEMES = theme/splash-320x320.png theme/splash-640x480.png
SVGURL = https://www.superquinquin.fr/wp-content/themes/superquinquin/img/superquinquin_logo_deule.svg

# The selected entry background is rendered by GRUB using a **9-slice**
# mechanism: 9 PNG images of 1×1 pixel covering positions `c nw n ne w e sw s # se`.
# All tiles share the same gold color "#f6d443", producing a solid rectangle
# with no rounded corners.
GRUBTHEMEBG   = installer/cdrom/boot/grub/themes/bg
GRUBMAP       = c nw n ne w e sw s se
GRUBMAPFILES  = $(GRUBMAP:%=$(GRUBTHEMEBG)/select_%.png)
INSTALLFILES += $(SPLASH) $(GRUBMAPFILES)

.INTERMEDIATE: $(SPLASH) $(GRUBMAPFILES)

theme/splash-320x320.png:
	magick -size 320x320 xc:white \( $(SVGURL) -resize 320x320 -trim \) \
	    -gravity Center -composite PNG24:$@

theme/splash-640x480.png:
	magick -size 640x480 xc:white \( $(SVGURL) -resize 200x200 -trim \) \
	    -gravity Center -composite PNG8:$@

installer/%/splash.png: $(THEMES)
	$(if $(filter $@,$(320_320)),cp theme/splash-320x320.png $@)
	$(if $(filter $@,$(640_480)),cp theme/splash-640x480.png $@)

theme/select.png:
	magick -size 1x1 xc:"#f6d443" PNG24:$@

$(GRUBTHEMEBG)/select_%.png: theme/select.png
	@mkdir -p $(dir $@)
	cp $< $@
