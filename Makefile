EXCLUSIONS := .DS_Store .directory \
				.git .gitmodules \
				.bash_history .bash_bookmarks \
				%.swp %~ %.pyc %.bak

SRCROOT    := src
CANDIDATES := $(wildcard $(SRCROOT)/.??*)
DOTFILES   := $(filter-out $(SRCROOT)/$(EXCLUSIONS), $(CANDIDATES))

all: help

help:
	@echo "make list          Show dot files in this repo"
	@echo "make deploy        Create symlink to home directory"
	@echo "make test          Display symlink commands"
	@echo "make update        Fetch changes for this repo"
	@echo "make install       Run make update, deploy, init"
	@echo "make clean         Remove the dot files and this repo"

list:
	@$(foreach val, $(DOTFILES), ls -dF $(val);)

deploy:
	@echo 'Start to deploy dotfiles to home directory...'
	@echo ''
	@$(foreach val, $(DOTFILES), ln -sfnv $(abspath $(val)) $(HOME)/$(notdir $(val));)

test:
	@echo '[TEST] Start to deploy dotfiles to home directory...'
	@echo ''
	@$(foreach val, $(DOTFILES), echo "ln -sfnv" $(abspath $(val)) $(HOME)/$(notdir $(val));)

update:
	git pull origin master
	git submodule init
	git submodule update
	git submodule foreach git pull origin master

install: update deploy
	@exec $$SHELL

clean:
	@echo 'Remove dot files in your home directory...'
	@-$(foreach val, $(DOTFILES), rm -vrf $(HOME)/$(notdir $(val));)
