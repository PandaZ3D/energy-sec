CONTIKI_PROJECT = energy_sec client-node server-node
all: $(CONTIKI_PROJECT)

CONTIKI = ../../../../..

include $(CONTIKI)/Makefile.dir-variables
MODULES += $(CONTIKI_NG_SERVICES_DIR)/simple-energest

# Include the CoAP implementation
MODULES += os/net/app-layer/coap

# MAKE_WITH_DTLS ?= 0

# ifeq ($(MAKE_WITH_DTLS),1)

#  TINYDTLS_PATH := os/net/security/tinydtls

#  ifeq (${wildcard $(CONTIKI)/$(TINYDTLS_PATH)/Makefile},)
#   ${error Could not find the tinyDTLS submodule. Please run "git submodule update --init" and try again}
#  endif

#  CFLAGS += -DWITH_DTLS=1

# #  MODULES += $(CONTIKI)/$(TINYDTLS_PATH)/contiki-support
#  MODULES += os/net/app-layer/coap/tinydtls-support # might need to write this
#  MODULES += $(TINYDTLS_PATH) ${addprefix $(TINYDTLS_PATH)/,aes sha2 ecc}

# endif

include $(CONTIKI)/Makefile.include

