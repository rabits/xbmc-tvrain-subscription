#!/bin/sh

REPO_DIR="xbmc_repo"

script_name=`basename $0`
script_path=`dirname $0`

cd $script_path

for plugin in ./plugin.*
do
	echo "Plugin: $plugin"
	find "$plugin" -name "*.pyc" -exec rm -rf {} \;
	find "$plugin" -name ".DS_Store" -exec rm -rf {} \;

	version=`cat $plugin/version.txt`
	addon_name=`basename $plugin`
	if [ ! -d "$REPO_DIR/$addon_name" ]; then
		mkdir "$REPO_DIR/$addon_name"
	fi
	rm -f "$REPO_DIR/$addon_name/$addon_name-$version.zip"
	zip -r "$REPO_DIR/$addon_name/$addon_name-$version.zip" "$addon_name" -X
done

python addons_xml_generator.py

mv -f addons.xml "$REPO_DIR/"
mv -f addons.xml.md5 "$REPO_DIR/"
