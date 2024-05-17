-- GT4 Used Car Script maker --

Automates the generation of used car scripts for Gran Turismo 4.

For use with GTSpecDB.Sqlite, Adhoc Toolchain, & Open Adhoc.
https://github.com/Nenkai/GTSpecDB/releases
https://github.com/Nenkai/GTAdhocToolchain
https://github.com/Nenkai/OpenAdhoc




Usage:
1. Dump your spec database into SQLite, then export the following tables into .csv:
	CAR_VARIATION_[region]
	GENERIC_CAR
	VARIATION[region]
	(The tool is expecting these three .csv files to have header rows, make sure they have them)

2. Add the dumped spec database files, and the gtmode project's [region]_carlist.ad from your modified game to the tool's database folder:
	CAR_VARIATION_[region].csv
	GENERIC_CAR.csv
	VARIATION[region].csv
	US_Carlist.ad

	Vanilla files are included, but if you have modified these files for your own game,
	replace them with your own.


3. Run `Step 1 Used car list maker.py`, and click each button in order, following
	the instructions at the top left corner of the pop-up windows.
	
	Each step will output a file in the database folder.
	When looking for the files the tool requests, they will be inside the database folder.

	If needed, you can check the outputted file at each step to verify there are no issues with
	your provided data.

	Important: Make sure there are no improperly added / incomplete entries to spec database tables, as this
	can cause errors. An example is an entry present in one table, but not properly present, or at all
	in the rest of them, when the script expects it.

	Step 1: Strips unnecessary columns from GENERIC_CAR, saves to new file

	Step 2: Adds variation column data from CAR_VARIATION_[region], saves to new file

	Step 3: Creates a list of cars to rule out, based on the cars found in [region]_carlist.ad
	This does not account for certain special cases that appear in the used car dealership, and
	also somewhere else. Special cases include the black edition variants,
	or cars that appear in the used dealership, but have a prize-only special color variant, such as 
	mgf_vvc_97, etc.
	Once this list is generated, you can remove the special cases from the rule out list as needed,
	and make sure to take note of which cars you removed from it before continuing.
	That way, the next steps will generate the used car entries for them, then you can
	selectively remove the specific variations that you do not want to appear in the used
	dealership.

		Special cases:
		1. All cars that have the Hide last color chip
		flag enabled are special cases that should be checked.
		- GENERIC_CAR --> GeneralFlags
		Use the included GeneralFlags reference sheet to check this flag.

		2. All prize cars present in [region]_carlist that have forced variations
		should be checked. Most if not all of these will also have hide last
		color chip also enabled, but it's important to also check for
		cars with forced variations and make sure there is a way to obtain the others.

		3. All prize cars present in [region]_carlist that aren't intended
		to be a prize exclusively, and is only obtainable elsewhere in the used car dealership.
		By default, no cars present in the list have this trait by itself,
		but if you edit your carlist to include such cars, this becomes a factor to consider.
		For example, adding a non-unique car without forced variations ("-") into the carlist,
		that you intend to also be buyable in the used car dealerships, and no where else.

		4. Poorly edited carlist scripts cause more special cases.
		Any car that is a prize for winning a
		license, mission, or completion % needs to be checked, as
		it can only be won once. If a car with multiple variations
		is assigned to a license prize or mission,
		another way to obtain the car should be considered.
		By default, the only car to consider is rx8_tmv_01,
		as its variation is forced to #1 without a way to obtain
		the other variations.
	
	
	Step 4: Removes cars based on the rule out list.

	Step 5: Creates a base list containing 1 of every unique car + variation combo,
	based on your game's specdb data and rules out cars contained in the rule out list.

	- If you removed special cases from the rule out list,
	you will need to edit the outputted Base list file after this step as well, removing
	any unwanted variations from it, leaving only the desired variations
	you want to appear in the used car dealerships.
	If you only want the special cases to appear at certain weeks or
	otherwise want to manually insert these, you'll need to take them out
	and take note of them separately for later manual placement in the scripts.

4. Run `Step 2 Used car week maker.py`. Browse and select the ouputted base list from the list maker,
	then set the number of dealers, if not three. Unless you've added more dealers than the standard trio
	of historic, early '90s and late '90s, this needs to stay at 3.
	Dealer 1: Historic (1989 and earlier)
	Dealer 2: Early '90's (1990 - 1995)
	Dealer 3: 1996 and newer

	Once the number of dealers is set, click `Set Dealer Ranges`.
	This will open a new window to set the possible quantity range
	in a given week for each dealer, and the valid year ranges for each dealer.
	So, if you desire to have a varying quantity of cars for sale in any given week,
	you can do so. Also, you can freely set the year ranges for each dealer.
	The tool will randomly choose a quantity value within your inputted range for
	the dealers each week. Then, it will pick cars that satisfy the
	specified year range for each dealer at random.
	
	Next, set the number of weeks, if not 100.
	By default, the game requires all 100 script files to be present
	in the game data, so you will only change this if you have
	already made the necessary changes to the game logic
	to use more or less weeks in the cycle.

	Next, set your dealer lineup sorting option. This tool provides 3 sorting methods to choose from:
	Completely random, no sorting
	Sort by model year (ascending), this is how the original game sorts the lineup.
	Sort by price (ascending)

	Last, you can set whether or not to have duplicate cars in the same week.
	Normally, the game does not have the same car appear more than once in the same week.

	Click `Generate Scripts`. The tool will first prioritize
	guaranteeing that each unique variation of each car is picked at least once,
	then once each car in every color has been picked once, it will
	start picking completely at random.
	
	The outputted .ad files will be located in ../usedcar_generated/

	This does not handle any special selections for the 100th week,
	such as the special black livery cars.
	So if you want to add them, you will need
	to write the 100th script manually.

	Also, this is the point at which you will make any manual edits to the
	scripts, do so before continuing.

5. In order to use these generated scripts, they will need to be compiled into .adc first.
	
	Run `Step 3 Batch ad compiler.py`.

	Specify which version of Adhoc to compile them to.
	By default, it is set to version 7, which corresponds
	to GT4 Online and Tourist Trophy.
	
	Specify the directories. If you want to perform rapid testing,
	you can directly set the output directory to the usedcar folder in your host filesystem.

	Click `Compile AD Files`, this will compile all .ad files inside the specified
	AD Files Directory and output them to your specified Output Directory.







