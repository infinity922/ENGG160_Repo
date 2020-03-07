/*
  FirmataEncoder.h - Firmata library
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

  FirmataEncoder handles instructions and is able to automatically report positions.
  See protocol details in "examples/SimpleFirmataEncoder/SimpleFirmataEncoder.ino"
*/

#ifndef FirmataEncoder_h
#define FirmataEncoder_h

#include <ConfigurableFirmata.h>
#include <FirmataFeature.h>

// This optional setting causes Encoder to use more optimized code
// safe if 'attachInterrupt' is never used in the same time
//#define ENCODER_OPTIMIZE_INTERRUPTS // => not compiling
#include <Zumo32U4Encoders.h>

#define MAX_ENCODERS                5 // arbitrary value, may need to adjust
#define LEFT_MOTOR_POWER            (0x00)
#define RIGHT_MOTOR_POWER           (0x01)
#define ENCODER_RESET_POSITION      (0x03)

class FirmataEncoder:public FirmataFeature
{
public:
  FirmataEncoder();
  //~FirmataEncoder(); => never destroy in practice

  // FirmataFeature implementation
  boolean handleSysex(byte command, byte argc, byte *argv);

  // FirmataEncoder implementation
  void setLeftMotorPower(byte powerA, byte powerB);
  void setLeftMotorPower(byte powerA, byte powerB);
  void reportPosition(byte encoderNum);
  void resetPosition(byte encoderNum);


private:
  static void _reportEncoderPosition(byte encoder, int16_t positionl, int16_t positionr);
};

#endif
