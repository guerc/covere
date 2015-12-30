#!/usr/bin/env python3

import hashlib
import sys
import shutil
import os

from argparse import ArgumentParser

parser = ArgumentParser(description="Copy SOURCE to TARGET with MD5-based verification and optional (secure) deletion of SOURCE")
parser.add_argument("-d", "--delete", action="store_true", help="remove SOURCE after copying")
parser.add_argument("-s", "--secure-delete", action="store_true", help="securely remove SOURCE after copying (shred)")
parser.add_argument("-v", "--verbose", action="store_true", help="show progress")
parser.add_argument("SOURCE", nargs="+")
parser.add_argument("TARGET")
argv = parser.parse_args()

def md5(fname):
	hash = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash.update(chunk)
	return hash.hexdigest()

sourceList = argv.SOURCE
targetDir = argv.TARGET

for item in sourceList:
	print("Copying ", item, "... ", sep="", end="", flush=True)
	shutil.copy2(item, targetDir)
	print("OK")

	print("Verifying ", item, "... ", sep="", end="", flush=True)

	if argv.verbose:
		print("\nHashing source... ", end="", flush=True)

	sourceHash = md5(item)

	if argv.verbose:
		print(sourceHash)
		print("Hashing target... ", end="", flush=True)

	targetHash = md5(targetDir.rstrip("/") + "/" + item)

	if argv.verbose:
		print(targetHash)

	if(sourceHash != targetHash):
		print("FAIL", "source MD5", sourceHash, "target MD5", targetHash)
		continue

	if not argv.verbose:
		print("OK")

	if argv.secure_delete:
		if argv.verbose:
			os.system("shred -ufvzn 0 \"" + item + "\"")
		else:
			os.system("shred -ufzn 0 \"" + item + "\"")
	elif argv.delete:
		if argv.verbose:
			print("Removing ", item, "... ", sep="", end="", flush=True)

		os.system("rm -f \"" + item + "\"")

		if argv.verbose:
			print("OK")