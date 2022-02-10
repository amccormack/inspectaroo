ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
# https://stackoverflow.com/a/10858332/228489
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

.PHONY: build check-env

build:
	@docker build . -t inspectaroo

dev: build check-env
	@docker run --rm -it \
		-e AWS_DEFAULT_REGION=us-east-2 \
		-e AWS_ACCESS_KEY_ID=${INS_ACCESS_KEY} \
		-e AWS_SECRET_ACCESS_KEY=${INS_SECRET_ACCESS_KEY} \
		-e AWS_SESSION_TOKEN=${INS_SESSION_TOKEN} \
		-v $(ROOT_DIR):/src/ -w /src/ inspectaroo bash

build-env:
	@bash writeenv.sh
	

check-env:
	@:$(call check_defined, INS_ACCESS_KEY)
	@:$(call check_defined, INS_SECRET_ACCESS_KEY)
	@:$(call check_defined, INS_SESSION_TOKEN)