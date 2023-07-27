#!/bin/bash

function dbresult {

mysql_user="root"
mysql_pass="mysql"
database="result"
table="results"
#execution_id="4.2.8RC06test1"

#sample_id="1"
#taskid="2"
#md5="2ab0a044780a55213d72e3e9cd2c331f"
#risk_score="10"
#profile="windows-7"
#build="JENKINS-20151217-2614-shark"
#hitpat=`curl -s -k -X GET https://$ma/rapi/tasks/$taskid/patterns?token=$token | grep group_name | sed -e 's/"pattern_group_name": "//g' | sed -e 's/"//g' | xargs | sed 's/.$//' | xargs`
#hitpat=`curl -s -k -X GET https://10.138.128.2/rapi/tasks/1/patterns?token=429a37905cf14af7a5c5bc5d0cd19e33 | grep group_name | sed -e 's/"pattern_group_name": "//g' | sed -e 's/"//g' | xargs | sed 's/.$//' | xargs`

echo "Uploading the result for $taskid in database"
### Check whether database exists or not ####
check_db=`mysqlshow --user=$mysql_user --password=$mysql_pass | grep -w $database | wc -l`
if [[ "$check_db" -eq 1 ]]
	then
		#echo "Database Existing"
		check_table=`mysql --user=$mysql_user --password=$mysql_pass -e "use $database;show tables" | grep -w $table | wc -l`
		#echo "check table value is" $check_table
		if [[ "$check_table" -eq 1 ]]
			then
				#echo "Required table in the database already existing."
				insert=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database;insert into $table (profile,md5,build,risk_score,execution_id, sample_id, task_id, patterns_hit, pattern_version) values ('"$profile"', '"$md5"', '"$build"', $risk_score, '"$execution_id"', $sample_id, $taskid, '$hitpat', '$pattern_version')";`
				#insert=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database;insert into $table (profile,md5,build,risk_score,execution_id, sample_id, task_id) values ('"$profile"', '"$md5"', '"$build"', $risk_score, '"$execution_id"', $sample_id, $taskid)";`
				$insert		
			else
				#echo "Required table in the database not existing. Creating the table."
				create_table=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database; create table $table (ID INT NOT NULL AUTO_INCREMENT primary key, sample_id  varchar(10), md5 varchar(50), risk_score INT);"`
				$create_table
				insert=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database;insert into $table (profile,md5,build,risk_score,execution_id, sample_id, task_id) values ('"$profile"', '"$md5"', '"$build"', $risk_score, '"$execution_id"', $sample_id, $taskid)";`
				echo "$insert"
		fi
		
	else	
		#echo "Database not existing."
		create_db=`mysql --user=$mysql_user --password=$mysql_pass --execute="create database $database;"`
		$create_db
		create_table=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database; create table $table (ID INT NOT NULL AUTO_INCREMENT primary key, sample_id  varchar(10), md5 varchar(50), risk_score INT);"`
		$create_table
		insert=`mysql --user=$mysql_user --password=$mysql_pass --execute="use $database;insert into $table (profile,md5,build,risk_score,execution_id, sample_id, task_id) values ('"$profile"', '"$md5"', '"$build"', $risk_score, '"$execution_id"', $sample_id, $taskid)";`
		$insert
fi

}
#dbresult
