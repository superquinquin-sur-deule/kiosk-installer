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

# authorized_keys
KEYS_FILE     = $(ASSETS)/var/lib/ansible/.ssh/authorized_keys
INSTALLFILES += $(KEYS_FILE)

.INTERMEDIATE: $(KEYS_FILE)

$(KEYS_FILE): ansible/group_vars/all.yml
	awk -F'[: "]+' '\
	    /^admin_keys:/ { f=1; next } \
	    /^[a-z]/       { f=0 } \
	    f && /^ +/     { print $$3, $$4, $$2 } \
	' $< > $@
	@test -s $@ || (echo "error: $<: no keys found"; exit 1)
