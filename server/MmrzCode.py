#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# universal:
MMRZ_CODE_Universal_OK = 0
MMRZ_CODE_Universal_Error = -40001
MMRZ_CODE_Universal_Verification_Fail = -40002

# signup:
MMRZ_CODE_Signup_OK = MMRZ_CODE_Universal_OK
MMRZ_CODE_Username_Not_Available_Error = -400011
MMRZ_CODE_Username_Not_Valid = -400012
MMRZ_CODE_Password_Not_Valid = -400013

# email
MMRZ_CODE_Email_Verification_OK = MMRZ_CODE_Universal_OK
MMRZ_CODE_Email_Send_OK = MMRZ_CODE_Universal_OK
MMRZ_CODE_Email_Address_Not_Changed = -400101
MMRZ_CODE_Email_Modification_Frequency_Limit_Error = -400102
MMRZ_CODE_Email_Send_Frequency_Limit_Error = -400103
MMRZ_CODE_Email_VeriCode_Out_Of_Date = -400104

# save & restore current state:
MMRZ_CODE_SaveState_Save_OK = MMRZ_CODE_Universal_OK
MMRZ_CODE_Restore_State_OK = MMRZ_CODE_Universal_OK
MMRZ_CODE_SaveState_Same_Eigenvalue = -400201
MMRZ_CODE_SaveState_Diff_Eigenvalue = -400202

