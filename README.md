Save the Prince!
==========================

Save the Prince (https://savetheprince.net) è un progetto originato dalla community [WWF YOUng Italia][0] volto a promuovere e coordinare gli sforzi dei volontari impegnati nei salvataggi degli anfibi dagli investimenti stradali: durante le migrazioni primaverili verso i luoghi di riproduzione, tale classe di sensibilissimi vertebrati (i primi a subire le pressioni del cambiamento climatico, delle malattie e della frammentazione degli habitat secondo la [IUCN][1]) subisce pesantissime perdite a causa degli investimenti durante l'attraversamento di arterie stradali. Spostandosi spesso in notturna, l'unico modo di ridurre tale impatto è rappresentato spesso dall'azione dei volontari, che con metodi adeguati spostano gli esemplari da una carreggiata all'altra della strada, allo stesso tempo memorizzando i dati del numero individui raccolti. 

L'azione è supportata da numerose associazioni, tra le quali [WWF Italia][2] e [SOS Anfibi][3].

...Per approfondire, c'è pure un [Little Talk][4]!

# Tecnologie
Il sito è costruito con [Python][4] usando il framework di sviluppo web [Django Web Framework][5] (usando come base un "Fantastic Project Starter", [Edge][6]) e il database [PostgreSQL][7] in congiunzione con la sua estensione spaziale [PostGIS][8].

Il progetto è composto dalle seguenti, semplici, applicazioni:

* profiles (gestione delle anagrafiche dei volontari e delle associazioni) 
* observations (memorizzazione delle osservazioni per i siti di salvataggio)
* news (microblogging)

### Quick start (più o meno)

Per lanciare velocemente il sito in locale, dopo aver copiato il *repository* è sufficiente installare
Python 3 e attivare l'ambiente virtuale (*pipenv*) all'interno del quale il progetto è impacchettato.

	pipenv install --python 3.6

Si installano quindi tutte le dipendenze:

    pipenv sync

Ed infine, si effettuano le migrazioni sul proprio database:

	cd src
    python manage.py migrate

Il sito, lavorando su una corposa parte geografica, lavora al meglio in congiunzione con un database PostgreSQL, che si può abilitare su distribuzioni Unix-Like come segue:

* Per la creazione dell'utente amdin:

	```bash
    sudo su postgres
    psql 
	```

* Per la creazione del database

	```psql
    CREATE USER admin WITH LOGIN SUPERUSER PASSWORD 'mioapassword';
    \q
	```


* Per l'abilitazione del database alla ricezione di richieste di connessione dall'esterno: 
	
	* in postgresql.conf 
	```bash	
    listen_addresses = "*"
    ```
    * in pg_hba.conf 
	```bash
    host	all	all	0.0.0.0/0	trust
	```	
* Per l'abilitazione dell'estensione spazializzante:

	```psql
	CREATE EXTENSION postgis;
	\q
	```
* 

[0]: https://www.wwf.it/tu_puoi/wwf_young/
[1]: https://en.wikipedia.org/wiki/List_of_endangered_amphibians
[2]: https://www.wwf.it
[3]: https://www.sosanfibi.it
[4]: https://www.facebook.com/WWFYOUng/videos/1585922534861522/
[5]: https://www.python.org/
[6]: https://www.djangoproject.com/
[7]: https://github.com/arocks/edge
[8]: https://www.postgresql.org
[9]: https://postgis.net

# Dedicato a...
Il sito è dedicato ad Enrico Romanazzi: che la sua memoria sia viva per sempre nell'animo di ogni rospista!
