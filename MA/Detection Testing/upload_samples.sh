#!/bin/bash

export PATH=$PATH:`pwd`
source mysql.sh
source settings.sh

if [ -z "$ma" ];
	then
		echo "Please provide an ip address where you would like to execute the tests."
		echo "Please declare the ipaddress in settings.txt file."
		exit
	else
		:
fi

echo -e "\nScript for Uploading Samples to MA"

####Generate Token####
token=`curl -s -k -X POST -d "username=$ma_adminuser&password=$ma_password" https://$ma/rapi/auth/session | grep token | cut -d':' -f2 | cut -d'"' -f2`
if [ -z "$token" ];
	then
		echo "Exiting the script since token is not generated. Manual interference is required to determine the root casue."
		echo "Bye bye have a great day !!"
		exit
	else
		:
fi
#####################

rm "$execution_id"result "$execution_id"task_id "$execution_id"task_newid "$execution_id"sample_id.txt "$execution_id"final_result.txt &> /dev/null
#mkdir taskreports &> /dev/null
rm -r taskreports/$execution_id &> /dev/null
mkdir -p taskreports/$execution_id
echo "Sample_ID TaskID md5 Build Pattern_version Risk_score " >> "$execution_id"final_result.txt

total_samples=`find $sample_dir -type f | wc -l`
echo "Total number of samples found are:" $total_samples

echo -e "Please wait uploading samples to " $ma "."

for entry in $(find $sample_dir)
	do	
		echo -e "Uploading sample $entry\r"
		`curl -s -k -X POST --form upload=@$entry --form owner=admin --form extension=exe https://$ma/rapi/samples/basic?token=$token | grep samples_sample_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"sample_id.txt`
	done
echo -e "Samples uploaded successfully"
echo -e "Creating task for each sample"
for sample_id in $(cat "$execution_id"sample_id.txt)
	do
	    case "$ma" in
			"10.138.128.180")
			if [ -z $plugin ]
				then
				#Win8
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win8&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
				else
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win8&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
			fi			
			;;
			
			"10.138.128.2"|"10.138.128.4"|"10.138.128.35"|"10.138.128.36"|"10.138.128.66"|"10.138.128.67"|"10.138.128.68")
			if [ -z $plugin ]
				then
					#win8
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win8&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#winxp
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$winxp&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#Win7
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#Win7x64
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7x64&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
				else
					#win8
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win8&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#winxp
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$winxp&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#Win7
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
					#Win7x64
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7x64&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
			fi
			;;
			
			"10.138.129.46")
			if [ -z $plugin ]
				then
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7x64&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
				else
					`curl -s -k -X POST -d "sample_id=$sample_id&env=$envtype&ivm_profile=$win7x64&tp_IVM.TIMEOUT=$timeout&tp_IVM.FIREWALL=$firewall&tp_DEF.log_task=$tasklog&tp_IVM.GET_DROPPED_FILES=$getdropfiles&tp_FILTER.SET.V1.FULL=$captureall&tp_DEF.ivm_plugin=_SYSTEM_:$plugin" https://$ma/rapi/tasks?token=$token | grep tasks_task_id | cut -d':' -f2 | cut -d',' -f1 | xargs -e >> "$execution_id"task_id`
			fi
			;;
		esac
	done 

for taskid in $(cat "$execution_id"task_id)
	do
		for (( i=0; i<=1000; i++ ))
		do 
			curl -s -k -X GET https://$ma/rapi/tasks/$taskid?token=$token | grep 'task_state_state' | head -1 | cut -d':' -f2 | cut -d',' -f1 | cut -d'"' -f2 > "$execution_id"task_state
			if [[ "`cat "$execution_id"task_state`" == "CORE_COMPLETE" ]]; 
				then 
					echo "Task ID "$taskid" completed successfully." >> "$execution_id"result;
					cat "$execution_id"result
					### Download pdf reports
					curl -s -o "taskreports/"$execution_id/$taskid.pdf -k -X GET 'https://'$ma'/rapi/widgets/task_report/'$taskid'?output=pdf&token='$token''
					### Get pattern version
					pattern_version=`curl -k -s -X GET https://$ma/rapi/system/version_info?token=$token | grep patterns_version | xargs | awk {'print $2'} | cut -d ',' -f1 | xargs`
					sample_id=`curl -s -k -X GET https://$ma/rapi/tasks/$taskid?token=$token | grep samples_sample_id | cut -d':' -f2 | cut -d',' -f1 | xargs`
					md5=`curl -s -k -X GET https://$ma/rapi/samples/$sample_id?token=$token | grep md5 |cut -d':' -f2 | cut -d',' -f1 | xargs` 
					risk_score=`curl -s -k -X GET https://$ma/rapi/tasks/$taskid?token=$token | grep global_risk_score | cut -d':' -f2 | cut -d',' -f1 | xargs`
					profile=`curl -s -k -X GET https://$ma/rapi/tasks/$taskid?token=$token | grep profiles_short_name | cut -d':' -f2 | cut -d',' -f1 | sed -e 's/"//g' | xargs`
					build=`curl -s -k -X GET https://$ma/rapi/system/version_info?token=$token | grep "mag2_version" | cut -d':' -f2 | cut -d',' -f1 | xargs`
					hitpat=`curl -s -k -X GET https://$ma/rapi/tasks/$taskid/patterns?token=$token | grep group_name | sed -e 's/"pattern_group_name": "//g' | sed -e 's/"//g' | xargs | sed 's/.$//' | xargs`
					echo "$sample_id $taskid $md5 $build $pattern_version $risk_score" >> "$execution_id"final_result.txt
					dbresult
					echo -e "\n"
					break; 
				else 
					echo "task "$taskid" still in process";
					sleep 1
			fi;
			#sleep 1; 
		done
	
	done
	
clear
column -t "$execution_id"final_result.txt
rm  "$execution_id"sample_id.txt "$execution_id"result "$execution_id"task_id "$execution_id"task_state "$execution_id"final_result.txt &> /dev/null

