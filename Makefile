.PHONY: install start enable status

install:
	sudo cp i_never_bot.service /etc/systemd/system/
	sudo systemctl daemon-reload

nano:
	nano .env
start:
	sudo systemctl start i_never_bot

enable:
	sudo systemctl enable i_never_bot

status:
	sudo systemctl status i_never_bot
