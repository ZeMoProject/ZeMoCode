#.profile file to autostart

Cyan='\033[1;36m'
NC='\033[0;0m'

echo -e "${Cyan}

 ZZZZZZZZZZZZZZ EEEEEEEEEEE MMM      MMM OOOOOOOOOO
 ZZZZZZZZZZZZZ  EEEEEEEEEEE MMMM    MMMM OOOOOOOOOO
         ZZZZ               MMMMMMMMMMMM OO      OO
       ZZZZ     EEEEEEEEEEE MMMMMMMMMMMM OO      OO
     ZZZZ       EEEEEEEEEEE MMM  MM  MMM OO      OO
   ZZZZ                     MMM      MMM OO      OO
  ZZZZZZZZZZZZ  EEEEEEEEEEE MMM      MMM OOOOOOOOOO
 ZZZZZZZZZZZZZ  EEEEEEEEEEE MMM      MMM OOOOOOOOOO

     @                 @                 @
    @@                @@                @@
   @@@@@     @       @@@@@     @       @@@@@     @
  @@@@@@@@  @@      @@@@@@@@  @@      @@@@@@@@  @@
 @@@@@@@@@@@@@     @@@@@@@@@@@@@     @@@@@@@@@@@@@
  @@@@@@@@  @@      @@@@@@@@  @@      @@@@@@@@  @@
   @@@@@     @       @@@@@     @       @@@@@     @
    @@                @@                @@
     @                 @                 @
${NC}"

if [ "x${SSH_TTY}" = "x" ]; then
sleep 10
fi
