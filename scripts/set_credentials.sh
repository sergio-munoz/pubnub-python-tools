#!/bin/bash
while IFS= read -r line;do
	export "$line" 
done < ~/Data/Git/pubnub-python-tools/.env