-- GT4 Used Wheel Script maker --

Automates the generation of used car scripts for Gran Turismo 4.

For use with GTSpecDB, Adhoc Toolchain, & Open Adhoc.
https://github.com/Nenkai/GTSpecDB/releases
https://github.com/Nenkai/GTAdhocToolchain
https://github.com/Nenkai/OpenAdhoc

Usage:
1. An important prerequisite is that you will need to add the wheel codes
	of any wheels that were not previously buyable at the wheel shop
	into the spec database WHEEL table. The game requires a unique ID
	assigned to each buyable wheel in order to apply the wheels to the
	car. Otherwise, the wheels will not apply once bought.

2. Run `Used wheels maker.py`, and paste in your desired wheel code list,
	completely unformatted.

	There is a full list of every wheel code included.

	The tool has a few options to define how the days get structured:
	
	You can divide the days into 3 different methods:
	1. Number of days: This will statically set the number of days in the total cycle,
	and automatically insert an equal amount of wheels into each day.
	
	2. Entries per section: This will statically set the number of wheels
	inserted into each day, and automatically generate days until all wheels have been selected.

	3. By manufacturer: This will divide the days by each wheel manufacturer,
	which is defined by the 1st 4 letters in the wheel codes.
	This will make each day only have every wheel from each manufacturer.

	4. Randomize Input List: Randomizes the selections.

3. After clicking `Process`, the formatted script will populate in the bottom box.
	You can repeatedly click the `Process` button to re-shuffle the selections
	if you want.

	Simply copy and paste the Formatted Output into your .ad file.

4. Compile your script with adhoc toolchain.