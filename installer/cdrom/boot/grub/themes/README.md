## GRUB Theme

Graphical theme for the GRUB installer (UEFI), visually aligned with
`isolinux.cfg` (BIOS).

### Asset generation

The selected entry background is rendered by GRUB using a **9-slice** mechanism:
9 PNG images of 1×1 pixel covering positions `c nw n ne w e sw s se`.
All tiles share the same gold color, producing a solid rectangle with no rounded corners.

```sh
cd installer/cdrom/boot/grub/themes/bg/
for f in c nw n ne w e sw s se; do
    magick -size 1x1 xc:"#f6d443" PNG24:select_$f.png;
done
```

Referenced in `theme.txt` via:

```
selected_item_pixmap_style = "bg/select_*.png"
```
