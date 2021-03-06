/*************************************************************************************************
Copyright (c) 2021 Keystone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
in the file COPYING.  If not, see <http://www.gnu.org/licenses/>.
**************************************************************************************************/
/** Avoid duplicate definitions */
#ifndef MASON_HDW_H
#define MASON_HDW_H

/** Avoid duplicate definitions */
#ifdef MASON_HDW_GLOBAL
#define MASON_HDW_EXT
#else
#define MASON_HDW_EXT extern
#endif

/** Header file reference */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h> //memcpy...
#include "mason_errno.h"
#include "mason_iap.h"

/** Compatibility with the cplusplus*/
#ifdef __cplusplus
extern "C"
{
#endif /* __cplusplus */

/** Macro definitions*/
#define PRV_KEY_LEN 32
#define PUB_KEY_LEN 64
#define SHA256_LEN 32
#define SHA512_LEN 64
#define RPMD160_LEN 20
#define HASH_LEN SHA256_LEN
#define MD5_LEN 16
#define SIG_LEN 64
#define CHECKSUM_LEN 4
#define SEED_LEN SHA512_LEN
#define DES3_KEY_LEN 24
#define DES3_IV_LEN 8
#define RSA_KEY_LEN 512

/* macro below mapped to gstHDWStatus value*/
#define HDW_STATUS_CHIP 0
#define HDW_STATUS_FACTORY 1
#define HDW_STATUS_ATTACK 2
#define HDW_STATUS_EMPTY 3
#define HDW_STATUS_WALLET 4
#define HDW_STATUS_MAX 5

	/** Variable definitions */
	MASON_HDW_EXT volatile uint8_t gDebugSwitchOn;
	typedef enum
	{
		E_HDWS_CHIP = 0x00,
		E_HDWS_FACTORY = 0xFA,
		E_HDWS_ATTACK = 0xA0,
		E_HDWS_EMPTY = 0xCB,
		E_HDWS_WALLET = 0x88,
		E_HDWS_MAX = 0x7FFFFFFF
	} emHDWStatusType;
	MASON_HDW_EXT volatile emHDWStatusType gemHDWStatus;

	typedef struct
	{
		emHDWStatusType emHDWStatus;
		char pSymbol[4];
	} stHDWStatusType;
	MASON_HDW_EXT const volatile stHDWStatusType gstHDWStatus[];

	typedef enum
	{
		E_HDWM_MNEMONIC = 0x00,
		E_HDWM_PASSPHRASE = 0x50,
	} emHDWSwitchType;
	MASON_HDW_EXT volatile emHDWSwitchType gemHDWSwitch;

	/** Function declarations */
	void mason_HDW_gen_sha256(uint8_t *pText, uint32_t textLen, uint8_t *pCheckSum, uint8_t checkSumLen);
	bool mason_HDW_check_sha256(uint8_t *pText, uint32_t textLen, uint8_t *pCheckSum);
	void mason_HDW_gen_sha256sha256(uint8_t *pText, uint32_t textLen, uint8_t *pCheckSum, uint8_t checkSumLen);
	bool mason_HDW_check_sha256sha256(uint8_t *pText, uint32_t textLen, uint8_t *pCheckSum);
	bool mason_get_mode(volatile stHDWStatusType *status);
	bool mason_set_mode(uint8_t type);
	emRetType mason_get_appvercode(uint32_t *vercode);
	emRetType mason_set_appvercode(void);

/** Compatibility with the cplusplus*/
#ifdef __cplusplus
} /* Extern C */
#endif

#endif
