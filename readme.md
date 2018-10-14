**Tech Used**<br>
Flask<br>
MongoDB<br>
Docker <br>

**Run Commands** <br>
*Requires python3/ Virtual Env not in included in the zip*<br>
pip3 install -r requirements.txt<br>
python3 app.py [for dev] <br>
 gunicorn app:app -w 1 --bind 0.0.0.0:9090 --reload [production] <br>

**Hosted At**<br>
https://udaan.bstark.tech/<br>

**Github**<br>
https://github.com/bhaskar-nair2/udaan_challenge.git<br>


**Routes** <br>
Ans 1: https://udaan.bstark.tech/screens ['POST'] <br>
Ans 2: https://udaan.bstark.tech/screens/pvr/reserve ['POST'] <br>
Ans 3: https://udaan.bstark.tech/screens/pvr/unreserved ['GET'] <br>
Ans 4: https://udaan.bstark.tech/screens/pvr/numSeats=3&choice=A7 ['GET'] <br>