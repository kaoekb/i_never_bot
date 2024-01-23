SERVICE_NAME = $(shell basename $(CURDIR))

.PHONY: install start enable status

install:
    sudo cp $(SERVICE_NAME).service /etc/systemd/system/
    sudo systemctl daemon-reload

start:
    sudo systemctl start $(SERVICE_NAME)

enable:
    sudo systemctl enable $(SERVICE_NAME)

status:
    sudo systemctl status $(SERVICE_NAME)
