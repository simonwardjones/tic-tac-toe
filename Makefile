################################################################
# Automated help script
# Please avoid using exactly two hash tags
################################################################
# To define help just add comment after command with 2 hashtags
# To add to section Use @@section name@@
################################################################

define python_help
import re
from collections import defaultdict

f = open('Makefile').read()
lines = re.findall(r"^[^#\\n\\r]*#{2}[^#\\n\\r]*?$$", f, re.MULTILINE)
makefile = defaultdict(list)
for line in lines:
	if len(re.findall(r"@@", line)) == 2:
		[(command, section, _help)] = re.findall(
			r"(.*?):.*?@@(.*?)@@(.*?)$$", line)
	elif len(re.findall(r"@@", line)) == 1:
		[(command, section, _help)] = re.findall(
			r"(.*?):.*?@@(\w+)(.*?)$$", line)
	else:
		[(command, _help)] = re.findall(
			r"(.*?):.*?#.*#(.*?)$$", line)
		section = "General"

	command = command.strip()
	section = section.strip().title()
	_help = _help.strip()
	makefile[section].append({
		"command": command,
		"help": _help
	})
BLUE = '\\x1b[34m'
GREEN = '\\x1b[32m'
CYAN = '\\x1b[36m'
GREY = '\\x1b[90m'
RED = '\\x1b[31m'
YELLOW = '\\x1b[33m'
RESET = '\\x1b[39m'

makefile_help = RED + """
Makefile help
""" + YELLOW + f"""
Commands:
To see command run: {CYAN}
   $$ make -n <command-name>

"""
command_max = max([len(y["command"])
				   for x in makefile.items()
				   for y in x[1]])
for section_name, commands in makefile.items():
	makefile_help += GREY + section_name + ":\\n"
	for command in commands:
		command_string = "{}{}{}{}".format(
			GREEN,
			command["command"].ljust(command_max + 5, "."),
			CYAN,
			command["help"])
		makefile_help += command_string + "\\n"
	makefile_help += "\\n" + RESET

print(makefile_help)
endef

export python_help



help: ## @@help Display this help and exit
	@echo "$$python_help" | python3


######################################################
# Automated help script ^^^^^
######################################################


proto:  ## @@proto commands@@Create the generated python for project
	python \
		-m grpc_tools.protoc \
		-I tic_tac_toe \
		--python_out=tic_tac_toe \
		--grpc_python_out=tic_tac_toe \
		tictactoe.proto 

run_random_player_x: ## @@tic tac@@ Run player X
	python tic_tac_toe/random_player_server.py -X

run_random_player_o: ## @@tic tac@@ Run player O
	python tic_tac_toe/random_player_server.py -O

run_game_service: ## @@tic tac@@ Run game service
	python tic_tac_toe/game_server.py

run_players_and_game: ## @@tic tac@@ Run palyers and game services
	make run_random_player_x & \
		make run_random_player_o & \
		make run_game_service &

make play_game: ## @@tic tac@@ Run palyers and game using services
	python tic_tac_toe/game_runner.py 