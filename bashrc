#.profile file to autostart

echo " ZZZZZZZZZZZZZZ EEEEEEEEEEE MMM      MMM OOOOOOOOOO
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
"
if [ "x${SSH_TTY}" != "x" ]; then
echo "Starting ZeMo Interface. Press Cntrl-C to exit."
sleep 15
echo "Zemo started"
fi