/*
  FirmataEncoder.cpp - Firmata library v0.1.0 - 2015-11-22
  Copyright (C) 2013 Norbert Truchsess. All rights reserved.
  Copyright (C) 2014 Nicolas Panel. All rights reserved.
  Copyright (C) 2015 Jeff Hoefs. All rights reserved.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  See file LICENSE.txt for further informations on licensing terms.

  Provide encoder feature based on PJRC implementation.
  See http://www.pjrc.com/teensy/td_libs_Encoder.html for more informations
*/

#include <ConfigurableFirmata.h>
#include <Zumo32U4Encoders.h>
#include <Zumo32U4Motors.h>
#include <string.h>
#include "FirmataEncoder.h"

#define isAttached(encoderNum) (encoderNum < MAX_ENCODERS && encoders[encoderNum])


static byte autoReport = 0x02;
static Zumo32U4Encoders u4Encoders;
static Zumo32U4Motors u4Motors

/* Constructor */
FirmataEncoder::FirmataEncoder()
{

}


/* Handle ENCODER_DATA (0x61) sysex commands
 * See protocol details in "examples/SimpleFirmataEncoder/SimpleFirmataEncoder.ino"
*/
void FirmataEncoder::handleCapability(byte pin) {}
boolean FirmataEncoder::handlePinMode(byte pin, int mode) {return false;}


boolean FirmataEncoder::handleSysex(byte command, byte argc, byte *argv)
{
  if (command == ENCODER_DATA)
  {
    byte encoderCommand, encoderNum, pinA, pinB, enableReports;

    encoderCommand = argv[0];

    if (encoderCommand == LEFT_MOTOR_POWER) {
        setLeftMotorPower(argv[1], argv[2]);
        return True;
    }

      if (encoderCommand == RIGH_MOTOR_POWER) {
          setRightMotorPower(argv[1], argv[2]);
          return True;
      }


    if (encoderCommand == ENCODER_REPORT_POSITION)
    {
      encoderNum = argv[1];
      reportPosition(encoderNum);
      return true;
    }


    if (encoderCommand == ENCODER_RESET_POSITION)
    {
      encoderNum = argv[1];
      resetPosition(encoderNum);
      return true;
    }


    //Firmata.sendString("Encoder Error: Invalid command");
  }
  return false;
}

void FirmataEncoder::reset(){}
void FirmataEncoder::setLeftMotorPower(byte powerA, byte powerB)
{
    int16_t power = powerA + 128*powerB;
    u4Motors.setLeftSpeed(power);

}
void FirmataEncoder::setRightMotorPower(byte powerA, byte powerB)
{
    int16_t power = powerA + 128*powerB;
    u4Motors.setRightSpeed(power);

}


void FirmataEncoder::resetPosition(byte encoderNum)
{
  int16_t re = u4Encoders.getCountsAndResetLeft();
  re = u4Encoders.getCountsAndResetLeft();
  reportPosition(1);
}

// Report specify encoder postion using midi protocol
void FirmataEncoder::reportPosition(byte encoder)
{

    Firmata.write(START_SYSEX);
    Firmata.write(ENCODER_DATA);

    _reportEncoderPosition(encoder, u4Encoders.getCountsLeft(),u4Encoders.getCountsRight());

    Firmata.write(END_SYSEX);

}
// Report all attached encoders positions (one message for all encoders)


void FirmataEncoder::_reportEncoderPosition(byte encoder, int16_t positionl, int16_t positionr)
{
  short absValuel = abs(positionl);
  short absValuer = abs(positionr);
  byte directionl = positionl >= 0 ? 0x00 : 0x01;
  byte directionr = positionr >= 0 ? 0x00 : 0x01;
  Firmata.write((directionl << 6) | (directionr));
  Firmata.write((byte)absValuel & 0x7F);
  Firmata.write((byte)(absValuel >> 7) & 0x7F);
  Firmata.write((byte)(absValuer) & 0x7F);
  Firmata.write((byte)(absValuer >> 7) & 0x7F);
}

