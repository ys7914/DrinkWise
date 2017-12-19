#include <Servo.h>
#include <ros.h>
#include <std_msgs/String.h>

//ros::init(argc,argv, "arduino_listener");

ros::NodeHandle nh;

std_msgs::String ros_msg;

ros::Publisher pub("arduino_listener", &ros_msg);

char f[2] = "f";


Servo servo1;
Servo servo2;


//String ingredients[] = {"apple", "orange", "mango", "berry"};

String menu[] = {"Paradise", "Martini", "Rose", "Manhattan", "Screwdriver", "Gibson", "Bacardi", "Americano"};

boolean recipes[8][4] = { {1, 1, 0, 0}, //Paradise
                        {1, 0, 1, 0}, //Martini
                        {1, 0, 0, 0}, //Rose
                        {0, 0, 1, 1}, //Manhattan
                        {1, 1, 1, 1}, //Screwdriver
                        {0, 0, 1, 0}, //Gibson
                        {0, 1, 0, 0}, //Bacardi
                        {0, 0, 0, 1}  //Americano
                        };

int current_position = 0;

//9 seconds for a full rotation
void quarter_turn(Servo& servo){
  servo.write(180);
  delay(2300);
  servo.write(90);
}

void eighth_turn(Servo& servo){
  servo.write(180);
  delay(1160);
  servo.write(90);
}

void make_drink(String from_ros){
  //run through the menu to find the index of the drink input
  int menu_index = 0;
  while(menu[menu_index] != from_ros){
    menu_index++;
  }
  if(menu_index > 7) return;

  
  //rotate carosel to correct places for drinks
  eighth_turn(servo1);
  if(recipes[menu_index][0]) delay(5000);
  quarter_turn(servo1);
  if(recipes[menu_index][1]) delay(5000);
  quarter_turn(servo1);
  if(recipes[menu_index][2]) delay(5000);
  quarter_turn(servo1);
  if(recipes[menu_index][3]) delay(5000);
  eighth_turn(servo1);

  ros_msg.data = f;
  pub.publish(&ros_msg);
  /*
  for(int i = 0; i < 4; i++){
    if(recipes[menu_index][i]){
      digitalWrite(13,HIGH);
      delay(5000);
      digitalWrite(13,LOW);  
    }
    quarter_turn(servo1);
    
  }
  */
  return;
}



int servo_control_pin_1 = 9;
int servo_control_pin_2 = 10;




void messageCb( const std_msgs::String& drink_msg){
  nh.loginfo(drink_msg.data);//message callback function
  make_drink(drink_msg.data);
  
}

ros::Subscriber<std_msgs::String> sub("arduino_listener", &messageCb ); //topic called drinks, calling messageCb function



void attach_servos(){
  servo1.attach(servo_control_pin_1);
  servo2.attach(servo_control_pin_2);
  return;
}


//this is blocking but i doubt we'll ever need it to not be
//20 rotations took ~16 seconds so purely by timing 1 roation should take 800ms
//^^MUCH FILTHY
//by experiment this was found to be 810ms backwards and 800ms forwards << SO MUCH FILTHY
void full_rotation(Servo& servo, boolean dir){
  servo.write(180*dir);
  delay(810 - 10*dir);
  servo.write(90);
}

void setup() {
  Serial.begin(57600);
  attach_servos();
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
  while(!nh.connected()) {nh.spinOnce();}
  nh.loginfo("All set up");
  
}

void loop() {
  nh.spinOnce();
  delay(10);
  //delay(1);
  
}
