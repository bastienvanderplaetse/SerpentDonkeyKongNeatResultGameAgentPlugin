 # SerpentDonkeyKongGamePlugin
_Author :_ Bastien VANDERPLAETSE  
_Description :_ Game plugin from SerpentAI Framework for Donkey Kong NES game. Realized in the context of a Master project in computing scientism.  
_Project Direction :_ Dr. Alexandre DECAN  
_Rapporteurs :_ Adrien COPPENS, Dr. Tom MENS  

This project requires the usage of the [SerpentAI Framework](https://github.com/SerpentAI/SerpentAI).

## Dependencies

* Conda (4.5.1)
* Python (3.6.3)
* SerpentAI (2018.1.2)
* fysom (2.1.5) (Not installed with SerpentAI !)
* numpy (1.14.1)
* scikit-learn (0.19.1)
* [Bizhawk](http://tasvideos.org/BizHawk.html)
* [Donkey Kong ROM](https://www.romstation.fr/games/donkey-kong-r36779)

## Important

* At first usage, an error will be displayed. It allows to create a default configuration file _donkeykong\_config.xml_.
* Change the value of the ```<title>``` tag by the title of the Bizhawk window.
* Change the value of the ```<emulator>``` tag by the path to the Bizhawk emulator.
* Change the value of the ```<game>``` tag by the path to the Donkey Kong ROM.
* When launching the GamePlugin, an error can be raised. In this case, just wait that Bizhawk has opened. The emulator takes a while before opening and the GamePlugin raises an error explaining that the Bizhawk window can not be focused. That is normal.