## Issues - At the time of developing this app
1. passlib doesn't support bcrypt 5.0> instead I used bcrypt "4.0.1". Installing passlib using "passlib[bcyrpt]"
will install the latest bcrypt. You have to install them seperately and specify a version for bcrypt