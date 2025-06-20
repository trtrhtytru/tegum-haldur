# tegum-haldur
Milleks seda kasutada?
See programm on graafiline süsteemi ressursside monitooringu rakendus ehk lihtne tegumihaldur. Sellega saab jälgida arvuti olulisi ressursse nagu CPU (protsessor), GPU (graafikakaart), RAM (mälu) ja kõvakettad reaalajas, näha nende kasutust graafikutena ning vaadata hetkel töötavaid protsesse ja nende CPU kasutust.
________________________________________
Koodi põhifunktsioonid:
1.	Kasutajaliides Tkinteriga:
Rakenduse aken on tehtud Pythonis Tkinteri raamistiku abil, mis loob akna ja erinevad infokastid (CPU, GPU, RAM, kõvakettad, protsesside nimekiri).
2.	Süsteemi info kogumine psutil-iga:
  o	CPU info: tuumade arv, loogilised lõimed, hetkekellata sagedus, protsessori kasutusprotsent.
  o	RAM info: kogu mälu suurus, kasutatud mälu protsent.
  o	Kõvakettad: partitsioonide vaba ruum ja kasutusprotsent.
  o	Protsesside nimekiri koos PID, nime ja CPU kasutusega.
3.	GPU info pärimine:
Kui arvutil on NVIDIA GPU ja nvidia-smi tööriist saadaval, küsitakse GPU nime, kasutust ja temperatuuri subprocess mooduli abil.
4.	Graafikute joonistamine Matplotlibi ja Tkinteri sees:
Kuvatakse reaalajas uuenevad joonisgraafikud CPU, GPU ja RAM kasutuse protsentidest viimase aja jooksul.
5.	Protsesside nimekiri:
Näidatakse kõige rohkem CPU kasutavaid protsesse ja uuendatakse nimekirja iga paari sekundi järel.
6.	Automaatne andmete uuendamine:
Kasutatakse Tkinteri after() funktsiooni, et iga 1–2 sekundi järel uuendada graafikuid, kettakasutust ja protsesside nimekirja.
________________________________________
Kokkuvõte:
See kood on projektiks, mis töötab Windows/Linux arvutis lihtsa tegumihaldurina, mis võimaldab kasutajal mugavalt ja visuaalselt jälgida arvuti ressursikasutust. See sobib näiteks süsteemi monitoorimiseks, diagnostikaks, või kui soovid oma arvuti koormust ja protsesse jälgida mugavalt ühes aknas.



Autorid: Denis Usakov, Denis Nikiforov, Tihon Patiteev 
