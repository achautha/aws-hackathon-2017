#!/usr/bin/env python
import sys, os
import boto3
import json
from optparse import OptionParser
import tempfile
import shutil
import zipfile

client = boto3.client('lex-models')


def dump_json(output, filename, tmp_dir, sub_dir=None):
    if not sub_dir:
        fname = tmp_dir + '/' + filename
    else:
        fname = tmp_dir + '/' + sub_dir + '/' + filename

    with open(fname, 'w') as fp:
        json.dump(output, fp, sort_keys=True, indent=4)


def fix_dates(mydict):
    if 'lastUpdatedDate' in mydict:
        mydict['lastUpdatedDate'] = str(mydict['lastUpdatedDate'])
    if 'createdDate' in mydict:
        mydict['createdDate'] = str(mydict['createdDate'])


def _export_bot(name, version="$LATEST", tmp_dir=None):
    bot_json_file = "{}_{}.json".format(name, version)
    print "Exporting bot {} as {}".format(name, bot_json_file)
    bot_output = client.get_bot(name=name, versionOrAlias=version)
    fix_dates(bot_output)
    dump_json(bot_output, bot_json_file, tmp_dir)
    return bot_output


def _export_intents(intents, tmp_dir=None):

    for intent in intents:
        intent_name = intent['intentName']
        intent_version = intent['intentVersion']

        print "Exporting intent {} {}".format(intent_name, intent_version)
        intent_out = client.get_intent(name=intent_name, version=intent_version)
        fix_dates(intent_out)
        intent_json_file = "{}_{}.json".format(intent_name, intent_version)
        dump_json(intent_out, intent_json_file, tmp_dir , "intents")

def _export_slot_types(intent, tmp_dir=None):
    intent_name = intent['intentName']
    intent_version = intent['intentVersion']
    intent_out = client.get_intent(name=intent_name, version=intent_version)
    slots = intent_out['slots']
    for s in slots:
        stype = s['slotType']
	if 'slotTypeVersion' in s:
            slot_type_out = client.get_slot_type(name=stype, version=s['slotTypeVersion'])
            fix_dates(slot_type_out)
            slot_json_file = "{}_{}.json".format(stype, s['slotTypeVersion'])
            dump_json(slot_type_out, slot_json_file, tmp_dir, "slots")
        else:
            print 'Ignore Built-in slot type {}'.format(stype) 

def export_all(name, version="$LATEST", tmp_dir=None):
    print "Exporting bot {} version {}".format(name, version)
    bot_out = _export_bot(name, version, tmp_dir)
    print "Exporting all intents as json files"
    _export_intents(intents=bot_out['intents'], tmp_dir=tmp_dir)
    print "Exporting all slot types as json files"
    for intent in bot_out['intents']:
        _export_slot_types(intent, tmp_dir)


def zip_it(tmp_dir, zip_file):
    cwd = os.getcwd()
    os.chdir(tmp_dir)
    zipf = zipfile.ZipFile(cwd + '/' + zip_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("."):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    os.chdir(cwd)

def _parse_args(args):
    required = ["bot_name", "zip_file"]
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")

    parser.add_option("-n", "--bot-name",
                      dest="bot_name",
                      help="Name of the AWS Lex bot",

                      )

    parser.add_option("-f", "--zip-file",
                      dest="zip_file",
                      help="Path of zip file")

    (options, args) = parser.parse_args()

    for r in required:
        if options.__dict__[r] is None:
            parser.error("parameter %s required" % r)

    return options.bot_name, options.zip_file


def main(args):
    bot_name, zip_file = _parse_args(args)
    tmp_dir = tempfile.mkdtemp()
    os.mkdir(tmp_dir + "/intents")
    os.mkdir(tmp_dir + "/slots")
    export_all(bot_name, tmp_dir=tmp_dir)
    print 'creating zip file'
    zip_it(tmp_dir, zip_file)
    print 'removing tmp directory'
    shutil.rmtree(tmp_dir)

#main
if __name__ == '__main__':
    main(sys.argv)

