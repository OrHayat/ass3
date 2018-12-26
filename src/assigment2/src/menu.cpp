#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"


int main(int argc, char **argv)
{
	

  ros::init(argc, argv, "ass2_menu");




  ros::NodeHandle n;//handler to ros system


  char buf [1024]={0};
  while (n.ok())
  {	
	printf(KBLU"insert 0 to exit the program\n");
	printf("insert 1 for moving the robot in line\n");
   	printf("insert 2 to rotate the robot\n");
	printf("insert 3 to check distance to object\n");
	printf("insert 4 to move and try to search for object\n"KNRM);
	fflush(stdout);
	int res=0,nitems;
	memset(buf,0,1024);
	char* tmpbuf=fgets(buf,1024,stdin);
	if(tmpbuf==NULL)
	{
	printf(KRED"failled to get input\n"KNRM);
	continue;
	}
	nitems = sscanf(buf,"%d", &res);
	if (nitems == EOF) {
	printf(KRED"failled to get input\n"KNRM);
	continue;	
	} else if (nitems != 1) {
	printf(KRED"failled to get input\n"KNRM);
	continue;
	} else 
	{
		if(res==0)
			{
				exit(-1);
			}
		else if(res==1)
			{
			system("rosrun assigment2 node1.py");
			continue;
			}
		else if(res==2)
		{
		system("rosrun assigment2 node2.py");
		continue;
		}
		else if(res==3)
		{
		system("rosrun assigment2 node3.py");
		continue;
		}
		else if(res==4)
		{
		system("rosrun assigment2 node5.py");
		continue;
		}
		else
		{
		printf(KRED"%d is illegal input \n"KNRM,res);
		}
	}
  }


  return 0;
}
