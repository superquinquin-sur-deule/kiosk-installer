# kiosk-installer
INSTALLER_FILES     = $(ASSETS)/etc/systemd/system/kiosk-installer.service
INSTALLER_FILES    += $(ASSETS)/etc/default/kiosk-installer
INSTALLFILES       += $(INSTALLER_FILES)

.INTERMEDIATE: $(INSTALLER_FILES)

INSTALLER_SERVICE   = ansible/roles/installer/templates/kiosk-installer.service

$(ASSETS)/etc/systemd/system/kiosk-installer.service: $(INSTALLER_SERVICE)
	cp $< $@

INSTALLER_DEFAULTS  = ansible/roles/installer/templates/kiosk-installer.j2
INSTALLER_DEFAULTS += ansible/roles/installer/defaults/main.yml

$(ASSETS)/etc/default/kiosk-installer: $(INSTALLER_DEFAULTS)
	awk -F': ' '\
	    NR==FNR { gsub(/"/, "", $$2); vars[$$1]=$$2; next } \
	    { for (v in vars) { \
	        regex="{{[[:space:]]*" v "[[:space:]]*}}"; \
	        gsub(regex, vars[v]) \
	    } print } \
	' $(word 2, $^) $< > $@
