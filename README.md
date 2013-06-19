# Sublime Text 2 Custom Vin65 Tag Support
This package adds support for Vin65 Custom tags to Sublime Text 2.

To add this package, navigate to the Sublime Text 2 Package directory. You can find this by typing ctrl/cmd+shift+p and then typing "Browse Packages".
Once you know the directory, open up your Git terminal and navigate there.
An example of navigating to this directory would be:
	cd ~/AppData/Roaming/Sublime\ Text\ 2/Packages
Now simply do a Git pull and Vin65 custom tag support will start working in HTML files once you restart Sublime.

## Tag Hints
If you want to add a pod you would type
	<v65pod
And Sublime will prompt you with tag options. Do not use the : in the tag name. This will be added automatically.

Once again using pods as an example, the default attributes of location and type will already be there for you.
Some attributes have their values prefilled for you. Simply type `t` and title will be prefilled. If you don't want any extra attributes, hit tab and then delete the comma at the end. Hit tab again and you will be taken outside the tag.

## Product Layouts
Tired of searching the documentation site for the product layout templates? Type one of the following and have the layout brought in automatically.
- product1Up
- product1UpStore
- product2Up
- product3Up
- product5Up
- productGroup
- productDrilldown
- productDrilldownStore